import datetime
import tensorflow as tf

class Model:
    def __init__(self, num_states, num_actions, batch_size):
        self.var_init = None
        self.num_states = num_states
        self.num_actions = num_actions
        self.batch_size = batch_size

        self._states = None
        self._actions = None

        self._logits = None
        self._optimiser = None
        self._saver = None

        self._define_model()

    def _define_model(self):
        self._states = tf.placeholder(shape=[None, self.num_states], dtype=tf.float32)
        self._q_s_a = tf.placeholder(shape=[None, self.num_actions], dtype=tf.float32)
        # create a couple of fully connected hidden layers
        fc1 = tf.layers.dense(self._states, 50, activation=tf.nn.relu)
        fc2 = tf.layers.dense(fc1, 50, activation=tf.nn.relu)
        self._logits = tf.layers.dense(fc2, self.num_actions)
        loss = tf.losses.mean_squared_error(self._q_s_a, self._logits)
        self._optimiser = tf.train.AdamOptimizer().minimize(loss)
        self.var_init = tf.global_variables_initializer()
        self._saver = tf.train.Saver()

    def predict_one(self, state, sess):
        return sess.run(self._logits, feed_dict={self._states: state.reshape(1, self.num_states)})

    def predict_batch(self, states, sess):
        return sess.run(self._logits, feed_dict={self._states: states})

    def train_batch(self, sess, x_batch, y_batch):
        sess.run(self._optimiser, feed_dict={self._states: x_batch, self._q_s_a: y_batch})

    def save(self, sess, path, cnt):
        _dt = datetime.datetime.now()
        save_path = self._saver.save(sess, f'{path}/model-{cnt}-{_dt.day}{_dt.month}{_dt.year}{_dt.hour}{_dt.minute}.ckpt')
        print('Model saved in path: %s' % save_path)

