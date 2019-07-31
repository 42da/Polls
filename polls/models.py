from django.db import models

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=10)
    introduction = models.TextField()
    area = models.CharField(max_length=15)
    party_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name

## 모델을 둘로나눔
## 1.홍보기간
class Poll(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    area = models.CharField(max_length=15)

## 2.후보자
class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete = models.CASCADE) ##어느투표에 대한 결과인지 알아야함
                                   #그래서 Poll 클래스에서 사용하고 있기 떄문에 불러오겠음
    Candidate = models.ForeignKey(Candidate, on_delete = models.CASCADE)#이미 있는 Candidate를 사용하기 위해 외부키지정
    votes = models.IntegerField(default=0)#득표수 받지 않았다면 0으로 하기 위해

