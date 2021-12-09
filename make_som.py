import numpy as np
import pickle
import somoclu
import yaml

#データを読み込んでデータとラベルに分離する
def read_data(path):
    with open(path) as f:
        L=f.readlines()
        L=L[1:]#1行目は特徴量ベクトルではないので読み飛ばす
    L=[i.replace("\n","").split(" ") for i in L]
    label=[i[-1] for i in L]
    data=[list(map(float,i[:-1])) for i in L]
    return np.array(data,dtype=np.float32),label

if __name__ == "__main__":
    with open("config.yaml") as f:
        config=yaml.safe_load(f)
    
    x,y=read_data(config["input_path"])

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