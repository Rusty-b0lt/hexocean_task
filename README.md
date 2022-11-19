# hexocean_task
## Set up
### Docker compose
- `docker compose build`
- `docker compose up -d`
### Inside container
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py createdefaultusertiers` - Custom script to create three default user tiers.
## API
### Uploading image
`POST http://localhost:8000/api/v1/image/`
`Form-Data: {"file": <file>}`
### Getting list of images
`GET http://localhost:8000/api/v1/image/`
### Creating an expiring link
`POST http://localhost:8000/api/v1/image/<id>/get_download_link/`
`JSON {"exp": <seconds>}`
### Admin
`http://localhost:8000/admin/`
