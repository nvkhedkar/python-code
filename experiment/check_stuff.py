import numpy as np

npl = np.array([0.1, 0.5, 2, 5, 100])
print("npl", npl)
print(npl + 1)
base = 1.01
lg_arr = np.log(npl + 1) / np.log(base)
print(lg_arr)
print(np.power(base, lg_arr) - 1)

BASE = 1.01
def preprocess_data_y(y_arr):
    print('preprocess_data_y')
    return np.log(y_arr + 1) / np.log(BASE)
    # return [np.power(arr, 1 / mod_value) for arr in y_arr]
    # return [np.power(arr, 1 / BASE) for arr in y_arr]
    # return [np.log(arr + 1) / np.log(BASE) for arr in y_arr]


def postprocess_results(y_arr):
    print('postprocess_results')
    return np.power(BASE, y_arr) - 1
    # return np.array([np.power(arr, mod_value) for arr in y_arr])
    # return [np.power(arr, BASE) for arr in y_arr]
    # return [np.power(BASE, arr) - 1 for arr in y_arr]


y_processed = preprocess_data_y(npl)
y_post = postprocess_results(y_processed)
print(f"y.shape: {npl.shape}, {y_processed.shape}, {y_post.shape}, {np.array_equal(npl, y_post)}")
print("npl".ljust(8), npl)
print(y_processed)
print("y_post".ljust(8), y_post)
