lines = [
        "Id  Features*   Architecture*   Loss name   L2 norm*    Learning rate*  Batch size  Evt. weights    Group weights   Dropout*    Batch norm.",
        "Default    lbn_light (74)  lbn_dense:30:default:128_128_128_128:tanh   wsgce   2E-03   5E-05   1024    TRUE    1.0, 1.0    0.1  TRUE",
        "51  lbn_light (74)  lbn_dense:30:default:128_128_128_128:tanh   wsgce   6E-03   1E-05   1024    TRUE    1.0, 1.0    0.05    TRUE",
        "39  lbn (121)   lbn_dense:30:default:128_128_128_128:tanh   wsgce   2E-02   1E-05   1024    TRUE    1.0, 1.0    0   TRUE",
        "131  lbn (121)   lbn_dense:30:extended:128_128_128_128:tanh  wsgce   6E-03   1E-05   1024    TRUE    1.0, 1.0    0   TRUE",
        "203  lbn_light (74)  lbn_dense:30:extended:256_256_256_256:tanh  wsgce   6E-04   1E-05   1024    TRUE    1.0, 1.0    0   TRUE",
        "280  lbn_light (74)  lbn_dense:30:extended:256_256_256_256:tanh  wsgce   2E-02   5E-05   1024    TRUE    1.0, 1.0    0.1  TRUE",
        "240  lbn_light (74)  lbn_dense:30:extended:256_256_256_256:tanh  wsgce   2E-03   5E-05   1024    TRUE    1.0, 1.0    0.05    TRUE",
        "12  lbn_light (74)  lbn_dense:30:default:128_128_128_128:tanh   wsgce   6E-04   5E-05   1024    TRUE    1.0, 1.0    0   TRUE",
        "43  lbn_light (74)  lbn_dense:30:default:128_128_128_128:tanh   wsgce   6E-04   1E-05   1024    TRUE    1.0, 1.0    0.05    TRUE",
]

for l in lines:
    stuff = l.split("  ")
    for i, s in enumerate(stuff):
        if not s.replace(" ", ""): continue
        print s.replace("_","\\_"), 
        if i != len(stuff) - 1: print "&",
    print "\\\\"
