In this part, you will learn the how to use [pyBIS](https://pypi.org/project/pybis/) to create new Projects and [Entities](https://datastore.bam.de/en/concepts/entity_and_entity_types) (Collections, Objects, Datasets), the parent-child relationships between Objects, as well as to automate the searchers/filtering of data in openBIS.

??? tip Testing the Python code
    We recommend the reader to launch a Jupyter Notebook in a Python environment with `pyBIS` installed, and run the commands shown throughout the next sections.

## Creating Projects and Other Entities

We can create new Projects by doing:

```python
new_project = o.new_project(
    code="<NEW-PROJECT-CODE>",
    space=my_space,
)
new_project.save()
```

!!! sucess 
    Do not forget to `save()` the newly created Projects or Entities after defining them.

To create a new Collection, we need to know the `type` we want to define. Nevertheless, in the BAM Data Store we only use `COLLECTION` types for any Collection:

```python
new_collection = o.new_collection(
    code="<NEW-COLLECTION-CODE>",
    type="COLLECTION",
    project=new_project,
)
new_collection.save()
```

### Creating New Objects

In order to create a new Object under a Collection or a Project, we need to know its `type` beforehand. This depends on the specific use-case where this is being applied, as this is the main building block of data modeling in openBIS (e.g., [Conceptual Data Model in the BAM Wiki](https://datastore.bam.de/en/How_to_guides/Represent_research_data)).

In this example, we will assume that we are creating a new experimental step and assigning some dummy metadata to it. 

We first create the Object:

```python
new_experimental_step = o.new_object(
    code="<NEW-OBJECT-CODE>",
    type="EXPERIMENTAL_STEP",
    collection=new_collection,
)
```

!!! note
    If we leave the `code` attribute empty, openBIS will automatically assign one based on the definition of `EXPERIMENTAL_STEP` followed by a 4-digit number (see [`generated_code_prefix` for `EXPERIMENTAL_STEP`](https://github.com/BAMresearch/bam-masterdata/blob/main/bam_masterdata/datamodel/object_types.py#L261)).

Each Object in openBIS has some assigned properties to it. A [Property](https://datastore.bam.de/en/concepts/property) is a metadata field used to describe such Object. It can be of different [data types](https://datastore.bam.de/en/masterdata_definition/best_practices#property-data-type) (e.g., string, integers, floats, etc.). One of the most relevant data types is [CONTROLLEDVOCABULARY](https://datastore.bam.de/en/concepts/controlled_vocabulary). These are specifically constrained values to a metadata field.

We can list the available properties of an Object by doing:

```python
new_experimental_step.props
# in dictionary format:
# new_experimental_step.props()
```

We can then define the properties by passing a dictionary:

```python
new_experimental_step.props = {
    "$name": : "trying out pybis",
    "finished_flag": False,
}
new_experimental_step.save()
```

Note that:
- Each property has a defined **data type**. If the stored value does not match the expected data type (e.g., `finished_flag` is a BOOLEAN, hence if you pass a string, e.g., `"False"`, pyBIS will return an error).
- Some properties are **mandatory** and some are **optional**. So if we save an object with some mandatory properties missing, we will get an error.
- The properties can be passed directly when creating a object: `new_object(..., props={...})`
- Alternatively, properties can be defined by using the key and assigning the value, e.g.: `new_experimental_ste["$name"]: "trying out pybis"`.

### Parent-child Relationships between Objects

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

We can delete parent-child relationships:

```python
parent_experimental_step.del_children(child_experimental_step)
parent_experimental_step.save()
```


### Attaching datasets

Datasets can be created similarly to other entities, with the exception that we need to specify files attached to it. We only use `RAW_DATA` as the Dataset type:

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

You've already learned in Part 1 to discover what is available in an openBIS instance. However, there are more advanced filters/searches that can be done, including filtering Objects whose metadata is a specific value or under a certain threshold value.

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

Here, the `props` attribute ensures that `$name` are returned in the result of the search.

We can also use mathematical operators (`>`, `<`, `=`, `>=`, `<=`):

```python
o.get_objects(registrationdate=">2023-07-21")
```

And more complex searches like:

```python
o.get_objects(
    space="MY_*",  # return from spaces starting with MY_
    type="*_STEP*",  # any objects that contain _STEP in the type
    withParents="*",  # containing any parents
    withChildren=[
        "/MY_SPACE/MY_PROJECT/MY_COLLECTION/SAMPLE*",
    ]  # containing children with code starting with SAMPLE
)
```
