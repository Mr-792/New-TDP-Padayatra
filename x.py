# import requests

# res=requests.post('http://localhost:8000/admin-signin/',data={"username":"hello"})
# print(res)


from Admins.models import Districts

my_dict={}
districts=Districts.objects.all()
for i in districts:
    my_dict[i.name]='nothing'
print(my_dict)