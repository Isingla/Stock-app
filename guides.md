# our flask guide

## add a user

```python
from app imoort db, user
db.create_all()
user = User(username="Sayam", email="test@gmail.com", password="test123456")
db.session.add(user)
db.session.commit()
```

## update a user

```
python
user=User.query.all()[0]
user.<attribute>= "assign a new value"
db.session.commit()

