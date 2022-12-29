from .models import Districts


my_dict={}

districts=Districts.objects.all()
for i in districts:
    my_dict[i.name]='nothing'
print(my_dict)