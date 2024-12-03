# Codes

---

## Run server
```
python manage.py runserver
```

## Database
```
### Generate models
python manage.py inspectdb > models.py

### Test postgres database
python manage.py dbshell

### Create an administrator account (Admin)
```bash
python manage.py createsuperuser

### Migration
```bash
python manage.py migrate
```

## Database operations
```python
####  查询所有 SampleData 对象
all_samples = SampleData.objects.all()

#### 查询特定条件的记录
sample = SampleData.objects.get(id=1)  # 根据主键查询单条记录

#### 查询满足条件的数据
samples = SampleData.objects.filter(gender=1)

#### 获取前10条记录
samples = SampleData.objects.all()[:10]

#### 按照 score 排序
samples = SampleData.objects.all().order_by('score')

#### 更新数据
sample = SampleData.objects.get(id=1)
sample.name = 'John Doe'
sample.save()  # 保存更改

#### 批量更新
SampleData.objects.filter(gender=1).update(score='100')  # 更新所有符合条件的记录

#### 创建并保存新的 SampleData
new_sample = SampleData(
    name='Jane Doe',
    birthdate='1995-01-01',
    score='95',
    grade='A',
    body_height='170cm',
    gender=0,
    phone='1234567890'
)
new_sample.save()  # 保存数据

#### 删除一条记录
sample = SampleData.objects.get(id=1)
sample.delete()  # 删除数据

#### 删除所有 gender 为 1 的记录
SampleData.objects.filter(gender=1).delete()
```


