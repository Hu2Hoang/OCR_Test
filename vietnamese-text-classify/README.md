## Download dataset
Download dataset vào thư mục `./data`
Link : [dataset](https://drive.google.com/drive/folders/1_DtQ9mB03p9OA6qa4zJlPawA1yAAHtDw?usp=sharing)

Download dataset vào thư mục `./model`
Link : [model](https://drive.google.com/drive/folders/1biCwmMgiIbVmniKq-BiDDRNvesl7K28o?usp=sharing)

## Training
- Install requirement
```
>> pip install -r requirements.txt
```
- Prepare data:
```
>> cd data/ && unrar x -r Test_Full.rar && unrar x -r Train_Full.rar

>> python load_data.py --data_path='data/'
```
- Train model 
```
>> python train.py --data_path="data/" --model_path="model/"
```
## Results
![png](images/accuracy.png)

- Classify text
```
>> python infer.py --prime "Đêm hôm qua, đội tuyển Việt Nam đã bay đến Trung Quốc chuẩn bị cho giải vô địch Châu Á."
```