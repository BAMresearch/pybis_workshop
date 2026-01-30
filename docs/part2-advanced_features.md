## Creating new entities

We can create new Projects by doing:

```python
new_project = o.new_project(
    code="<NEW-PROJECT-CODE>",
    space=my_space,
)
new_project.save()
```

For creating a new Collection, we need to know the `type` we want to define. Nevertheless, in the BAM Data Store we only use `COLLECTION` types for any Collection:

```python
new_collection = o.new_collection(
    code="<NEW-COLLECTION-CODE>",
    type="COLLECTION",
    project=new_project,
)
new_collection.save()
```

Knowing the Object type before creating one is important and the main objective of data modeling. In this example, we will assume that we are creating a new experimental step and assigning some dummy metadata to it. For that, we first create the Object:

```python
new_experimental_step = o.new_object(
    code="<NEW-OBJECT-CODE>",
    type="EXPERIMENTAL_STEP",
    collection=new_collection,
)
```

Note:
    - We can leave `code` empty and the system will automatically assign one based on the definition of `EXPERIMENTAL_STEP`.

We now assign properties. We can list the properties of an object by doing:

```python
new_experimental_step.props
```

Or a dictionary instead:

```python
new_experimental_step.props()
```

We can then define the properties by passing a dictionary:

```python
new_experimental_step.props = {
    "$name": : "trying out pybis",
    "finished_flag": False,
}
```

And save:

```python
new_experimental_step.save()
```

Notes:
- Some properties are mandatory and some are optional. So if we save an object with some mandatory properties missing, we will get an error.
- The properties can be passed directly when creating a object: `new_object(..., props={...})`
- Alternatively, properties can be defined by using the key and assigning the value, e.g.: `new_experimental_ste["$name"]: "trying out pybis"`

### Parent-child relationships

Following the previous steps, imagine we create two additional experimental steps: `parent_experimental_step` and `child_experimental_step`.

We can then create a parent-child relationship for our `new_experimental_step`:

```python
new_experimental_step.parents = parent_experimental_step
new_experimental_step.children = child_experimental_step
new_experimental_step.save()
```

We can also add parents or children using the synthax:

```python
parent_experimental_step.add_children(child_experimental_step)
parent_experimental_step.save()
```

We can also delete parent-child relationships:

```python
parent_experimental_step.del_children(child_experimental_step)
parent_experimental_step.save()
```


### Attaching datasets

Datasets can be created similarly to other entities, with the exception that we need to specify files. We only use `RAW_DATA` as the Dataset type:

```python
new_dataset = o.new_dataset(
    type="RAW_DATA",
    object=new_experimental_step,
    files=["path-to-some-file"]
)
new_dataset.save()
```

We can also delete them:

```python
new_dataset.delete(reason="We finished with the example")
```


## Search and Filters

We already learned how to discover what is in an openBIS instance. However, there are more advanced filters/searches that can be done to automate this step.

We will consider filtering Objects in this example.

Typically, `get_objects()` and the similar methods return all the objects in an instance. For efficiency, it is better to create batches and loop over them to map the objects with the desired properties. We can then use the `count` and `start_with` parameters to code this:

```python
start_with = 3 

experimental_steps = o.get_objects(type="EXPERIMENTAL_STEP", count=6, start_with=start_with)
```

`start_with`  specifies which element in the list of `get_objects()` to start with, while `count` returns a specific number of elements from the search. We use `type` to define the type of objects we want to return.

```python
for step in experimental_steps:
    print(f"Experimental step: {step.code}")
```

We can also get objects whose properties match certain values:

```python
o.get_objects(where={"$name": "* <name-we-want-to-find>"}, props=["$name"])
```

Here, `props` ensures that `$name` are returned in the result of the search.

We can also use mathematical operators (`>`, `<`, `=`, `>=`, `<=`):

```python
o.get_objects(registrationdate=">2023-07-21")
```

And more complex searches like:

```python
o.get_objects(
    space="MY_*",  # return from spaces starting with MY_
    type="*_STEP*",  # return any objects that contain _STEP in the type
    withParents="*",  # with any parents
    withChildren=[
        "/MY_SPACE/MY_PROJECT/MY_COLLECTION/SAMPLE*",
    ]  # with children with code starting with SAMPLE
)
```
