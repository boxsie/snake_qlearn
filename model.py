import tensorflow as tf

class Model:
    def __init__(self, num_states, num_actions, batch_size, learning_rate, grid_size, frames_per_state):
        self.var_init = None
        self.num_states = num_states
        self.num_actions = num_actions
        self.batch_size = batch_size
        self._learning_rate = learning_rate
        self._grid_size = grid_size
        self._frames_per_state = frames_per_state

        self._states = None
        self._actions = None

        self._logits = None
        self._optimiser = None
        self._saver = None

        self._define_model()

    def _define_model(self):
        self._states = tf.compat.v1.placeholder(shape=[None, self.num_states], dtype=tf.float32)
        self._qsa = tf.compat.v1.placeholder(shape=[None, self.num_actions], dtype=tf.float32)

        cnn_shaped = tf.reshape(self._states, [-1, self._grid_size, self._grid_size, self._frames_per_state])

        conv1 = self._create_cnn_layer(
            input_data=cnn_shaped,
            num_channels=self._frames_per_state,
            num_filters=32,
            filter_shape=[5, 5],
            pool_shape=[2, 2],
            name='conv1'
        )
        conv2 = self._create_cnn_layer(
            input_data=conv1,
            num_channels=32,
            num_filters=64,
            filter_shape=[5, 5],
            pool_shape=[2, 2],
            name='conv2'
        )
        flattened = tf.reshape(conv2, [-1, int(((self._grid_size * 0.25) ** 2) * 64)])
        fc1 = tf.layers.dense(flattened, 32, activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, 32, activation=tf.nn.relu)
        self._logits = tf.layers.dense(fc2, self.num_actions)
        loss = tf.losses.mean_squared_error(self._qsa, self._logits)
        self._optimiser = tf.train.AdamOptimizer(learning_rate=self._learning_rate).minimize(loss)
        self.var_init = tf.global_variables_initializer()
        self._saver = tf.train.Saver()

    def predict_one(self, state, sess):
        return sess.run(self._logits, feed_dict={self._states: state.reshape(1, self.num_states)})

    def predict_batch(self, states, sess):
        return sess.run(self._logits, feed_dict={self._states: states})

    def train_batch(self, sess, x_batch, y_batch):
        sess.run(self._optimiser, feed_dict={self._states: x_batch, self._qsa: y_batch})

    def save(self, sess, path, filename):
        save_path = self._saver.save(sess, f'{path}/{filename}.ckpt')
        print(f'\nModel saved in path: {path}/{filename}.ckpt')

    def load(self, sess, path, filename):
        self._saver.restore(sess, f'{path}/{filename}.ckpt')
        print(f'\nModel loaded from path: {path}/{filename}.ckpt')

    def _create_cnn_layer(self, input_data, num_channels, num_filters, filter_shape, pool_shape, name):
        shape = [filter_shape[0], filter_shape[1], num_channels, num_filters]

        weights = tf.Variable(tf.random.truncated_normal(shape, stddev=0.03, name=f'{name}_W'))
        bias = tf.Variable(tf.random.truncated_normal([num_filters]), name=f'{name}_b')

        out_layer = tf.nn.conv2d(input_data, weights, [1, 1, 1, 1], padding='SAME')
        out_layer += bias
        out_layer = tf.nn.relu(out_layer)

        ksize = [1, pool_shape[0], pool_shape[1], 1]
        strides = [1, 2, 2, 1]
        out_layer = tf.nn.max_pool2d(out_layer, ksize=ksize, strides=strides, padding='SAME')

        return out_layer

