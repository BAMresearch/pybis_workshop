Every new application of pyBIS implies first connecting to the specific instance you want to work with.

Define some variables:

```python
URL = "<https-path-to-openbis-instance>"
USERNAME = "<your-bam-username>" 
PASSWORD = "<your-password>
```

!!! warning 
    Note that you **must not** openly distribute your username and password. Make sure that, before pushing content to GitHub or any open-access, public service, these are deleted or anonymized. There are other implementations explained online (or by ChatGPT) which can help you add your username/passwords securely.

You can log in openbis with:
```python
from pybis import Openbis

o = Openbis(URL)
o.login(USERNAME, PASSWORD)
```

After a few seconds, `o` will connect with your credentials to the openBIS instance specified in `URL`.

We can check if the session is active:
```python
o.is_session_active()()
```

Or check the openBIS version:

```python
o.get_server_information().openbis_version
```

We can also define a personal access token (PAT):
```python
PAT = o.get_or_create_personal_access_token(sessionName="Session Whatever")
```

And use it for login instead of the username and password
```python
o = Openbis(URL)
o.set_token(PAT, save_token=True)
```

## Exploring the openBIS available entities

### Spaces and Projects

```python
o.get_spaces()
```

```python
my_space = o.get_spaces("<SPACE-CODE>")
```

Then, we can get a specific project from that space:
```python
my_project = my_space.get_project("<PROJECT-CODE>")
```

In order to know the available projects defined in an instance:
```python
o.get_projects()
```

!!! hint 
    Note that the plural (get_spaces, get_projects) is used on an `Openbis` instance to return the available entities in that instance. The singular is then used for one single entity (space, project, or any other).

### Collections

We can list all collections in an instance, space, or project by respectively doing:

```python
o.get_collections()
my_space.get_collections()
my_project.get_collections()
```

We can also specify one based on the path:

```python
my_collection = o.get_collection("/<SPACE-CODE>/<PROJECT-CODE>/<COLLECTION-CODE>")
```

Or with a `permID` (found when using `get_collections()`):

```python
my_collection = o.get_collection(permID)
```

### Objects and Datasets

Objects can also be found equivalently to Collections. The only difference is that an Object might be either attached to a Project or to a Collection:

```python
o.get_objects()
my_space.get_objects()
my_project.get_objects()
my_collection.get_objects()
```

Or by the specific path or permID:

```python
my_object = o.get_object("/<SPACE-CODE>/<PROJECT-CODE>/<COLLECTION-CODE>/<OBJECT-CODE>")
my_object = o.get_object("/<SPACE-CODE>/<PROJECT-CODE>/<OBJECT-CODE>")
my_object = o.get_object(permID)
```

Datasets follow the same functionalities with `get_datasets()` and `get_dataset()`, and can be attached to Collections or Objects. We can also download a specific dataset (e.g., defined by a `permID`):

```python
o.get_dataset(permID).download()
```

And even specify the path directory where to download:

```python
o.get_dataset(permID).download(destination="my_downloads", create_default_folders=False)
```


