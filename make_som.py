import numpy as np
import os
import pickle
import somoclu
import yaml

#データを読み込んでデータとラベルに分離する
def read_data(path):
    with open(path) as f:
        L=f.readlines()
        print("features:",L[0])
        L=L[1:]#1行目は特徴量ベクトルではないので読み飛ばす
    L=[i.replace("\n","").split(" ") for i in L]
    label=[i[-1] for i in L]

    print("start make data")
    data=np.array([list(map(float,i[:-1])) for i in L],dtype=np.float32)
    print("end make data")
    return data,label

if __name__ == "__main__":
    with open("config.yaml") as f:
        config=yaml.safe_load(f)
    
    print("start read data")

    base_name=config["input_path"].split(".")[0]
    data_pickle=base_name+"_data.pickle"
    label_pickle=base_name+"_label.pickle"

    #pickleが保存してあったらそこから読み込む
    if os.path.isfile(data_pickle) and os.path.isfile(label_pickle):
        print("load pickle")
        with open(data_pickle,"rb") as f:
            x=pickle.load(f)

        with open(label_pickle,"rb") as f:
            y=pickle.load(f)
    else:
    x,y=read_data(config["input_path"])
        #pickle形式で保存
        print("save pickle")
        with open(data_pickle,"wb") as f:
            pickle.dump(x,f)
        with open(label_pickle,"wb") as f:
            pickle.dump(y,f)

    #SOMの定義
    n_rows=config["n_rows"]
    n_cols=config["n_cols"]
    som=somoclu.Somoclu(n_rows=n_rows,n_columns=n_cols,
                        maptype=config["maptype"],initialization="random",
                        verbose=2,compactsupport=False)

    #学習
    som.train(data=x,epochs=config["epochs"])

    #コードブックの保存
    with open(config["codebook_path"],"wb") as f:
        pickle.dump(som.codebook,f)
    
    #umatrixの保存
    with open(config["umatrix_path"],"wb") as f:
        pickle.dump(som.umatrix,f)

    #somの表示・保存
    som.view_umatrix(labels=y,bestmatches=True)
    som.view_umatrix(labels=y,bestmatches=True,filename=config["som_path"])