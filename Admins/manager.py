from django.contrib.auth.base_user import BaseUserManager

class AdminManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,username,password=None,**extra_fields):
        if not username:
            raise ValueError('Username is Required')
        user=self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(self._db)

    def create_superuser(self,username,password,**extra_feilds):
        extra_feilds.setdefault('is_staff',True)
        extra_feilds.setdefault('is_superuser',True)
        extra_feilds.setdefault('is_active',True)
        extra_feilds.setdefault('is_superadmin',True)
        extra_feilds.setdefault('is_supervisor',True)
        extra_feilds.setdefault('is_manager',True)

        return self.create_user(username,password,**extra_feilds)

    def create_manager(self,username,password,**extra_feilds):
        extra_feilds.setdefault('is_staff',True)
        extra_feilds.setdefault('is_superuser',False)
        extra_feilds.setdefault('is_active',True)
        extra_feilds.setdefault('is_superadmin',False)
        extra_feilds.setdefault('is_supervisor',False)
        extra_feilds.setdefault('is_manager',True)

        return self.create_user(username,password,**extra_feilds)
        
    def create_supervisor(self,username,password,**extra_feilds):
        extra_feilds.setdefault('is_staff',True)
        extra_feilds.setdefault('is_superuser',False)
        extra_feilds.setdefault('is_active',True)
        extra_feilds.setdefault('is_superadmin',False)
        extra_feilds.setdefault('is_supervisor',True)
        extra_feilds.setdefault('is_manager',False)

        return self.create_user(username,password,**extra_feilds)
        
              
