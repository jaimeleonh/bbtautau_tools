#! /usr/bin/env python

def get_theo_xs(kl=1.0, cv=1.0, c2v=1.0):
    import HHModel as HHModel

    s1 = HHModel.VBF_sample_list[0].val_xs
    s2 = HHModel.VBF_sample_list[1].val_xs
    s3 = HHModel.VBF_sample_list[2].val_xs
    s4 = HHModel.VBF_sample_list[3].val_xs
    s5 = HHModel.VBF_sample_list[4].val_xs
    s6 = HHModel.VBF_sample_list[5].val_xs

    val = s1 * (-3.3 * (c2v ** 2) + 1.3 * c2v * (cv ** 2) + 7.6 * c2v * cv * kl
        + 2.0 * (cv ** 4) - 5.6 * (cv ** 3) * kl - 1.0 * (cv ** 2) * (kl ** 2))\
        + s2 * (1.5 * (c2v ** 2) + 0.5 * c2v * (cv ** 2) - 4.0 * c2v * cv * kl
        - 2.0 * (cv ** 4) + 4.0 * (cv ** 3) * kl)\
        + s3 * (0.35 * (c2v ** 2) - 0.0166666666666667 * c2v * (cv ** 2)
        - 1.03333333333333 * c2v * cv * kl - 0.333333333333333 * (cv ** 4)
        + 0.533333333333333 * (cv ** 3) * kl + 0.5 * (cv ** 2) * (kl ** 2))\
        + s4 * (-0.45 * (c2v ** 2) + 0.45 * c2v * (cv ** 2) + 0.9 * c2v * cv * kl + 1.0 * (cv ** 4)
        - 2.4 * (cv ** 3) * kl + 0.5 * (cv ** 2) * (kl ** 2))\
        + s5 * (-2.0 * (c2v ** 2) - 3.33333333333333 * c2v * (cv ** 2)
        + 9.33333333333333 * c2v * cv * kl + 5.33333333333333 * (cv ** 4)
        - 9.33333333333333 * (cv ** 3) * kl)\
        + s6 * (0.4 * (c2v ** 2) - 0.4 * c2v * (cv ** 2)
        - 0.8 * c2v * cv * kl + 0.8 * (cv ** 3) * kl)

    return val
