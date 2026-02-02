In this part, you will learn how to use [pyBIS](https://pypi.org/project/pybis/) to create new Projects and [Entities](https://datastore.bam.de/en/concepts/entity_and_entity_types) (Collections, Objects, Datasets), define parent-child relationships between Objects, and define advanced searches and filters in openBIS.

??? tip Testing the Python code
    We recommend that readers launch a Jupyter Notebook in a Python environment with `pyBIS` installed, and run the commands shown throughout the following sections.

## Creating Projects and other Entities

You can create new Projects as follows:

```python
new_project = o.new_project(
    code="<NEW-PROJECT-CODE>",
    space=my_space,
)
new_project.save()
```

!!! sucess 
    Do not forget to call `save()` on newly created Projects or Entities after defining them to store them in openBIS.

To create a new Collection, we need to know the `type` we want to define. Nevertheless, in the BAM Data Store we only use `COLLECTION` types is used for any Collection:

```python
new_collection = o.new_collection(
    code="<NEW-COLLECTION-CODE>",
    type="COLLECTION",
    project=new_project,
)
new_collection.save()
```

### Creating new Objects

To create a new Object under a Collection or a Project, we need to know its `type` beforehand. This depends on the specific use case, as Object types are the main building blocks of data modeling in openBIS (see, e.g., the [Conceptual Data Model in the BAM Wiki](https://datastore.bam.de/en/How_to_guides/Represent_research_data)). 

You can find all available Object types in the [BAM Masterdata repository](https://github.com/BAMresearch/bam-masterdata/blob/main/bam_masterdata/datamodel/object_types.py) or in the openBIS Admin UI.

In this example, we assume that we are creating a new experimental step and assigning some dummy metadata to it. 

First, create the Object:

```python
new_experimental_step = o.new_object(
    code="<NEW-OBJECT-CODE>",
    type="EXPERIMENTAL_STEP",
    collection=new_collection,
)
```

!!! note
    If the `code` attribute is left empty, openBIS will automatically assign one based on the definition of `EXPERIMENTAL_STEP`, followed by a four-digit number (see [`generated_code_prefix` for `EXPERIMENTAL_STEP`](https://github.com/BAMresearch/bam-masterdata/blob/main/bam_masterdata/datamodel/object_types.py#L261)).

Each Object in openBIS has a set of assigned properties. A [Property](https://datastore.bam.de/en/concepts/property) is a metadata field used to describe an Object. Properties can have different [data types](https://datastore.bam.de/en/masterdata_definition/best_practices#property-data-type) (e.g., string, integers, floats, etc.). One of the most relevant data types is [CONTROLLEDVOCABULARY](https://datastore.bam.de/en/concepts/controlled_vocabulary), which restricts values to a predefined set.

You can list the available properties of an Object by doing:

```python
new_experimental_step.props
# in dictionary format:
# new_experimental_step.props()
```

You can store metadata in the properties by passing a dictionary:

```python
new_experimental_step.props = {
    "$name": : "trying out pybis",
    "finished_flag": False,
}
new_experimental_step.save()
```

Note that:

* Each property has a defined **data type**. If the provided value does not match the expected type (e.g., `finished_flag` is a BOOLEAN, so passing `"False"` as a string will raise an error).
* Some properties are **mandatory**, while others are **optional**. Saving an Object with missing mandatory properties will result in an error.
* Properties can be passed directly at Object creation time using: `new_object(..., props={...})`
* Alternatively, properties can be set individually, for example: `new_experimental_step["$name"]: "trying out pybis"`.

### Parent-child Relationships between Objects

Following the previous steps, imagine creating two additional experimental steps: `parent_experimental_step` and `child_experimental_step`.

Now, you can create a parent-child relationship for `new_experimental_step`:

```python
new_experimental_step.parents = parent_experimental_step
new_experimental_step.children = child_experimental_step
new_experimental_step.save()
```

You can also add parents or children using the following syntax:

```python
parent_experimental_step.add_children(child_experimental_step)
parent_experimental_step.save()
```

You can delete parent-child relationships as well:

```python
parent_experimental_step.del_children(child_experimental_step)
parent_experimental_step.save()
```


### Attaching datasets

Datasets can be created similarly to other entities, with the difference that files must be attached. In the BAM Data Store, only `RAW_DATA` is used as the Dataset type:

```python
new_dataset = o.new_dataset(
    type="RAW_DATA",
    object=new_experimental_step,
    files=["path-to-some-file"]
)
new_dataset.save()
```

Datasets can also be deleted:

```python
new_dataset.delete(reason="We finished with the example")
```

## Search and filters

In Part 1, you learned how to explore what is available in the openBIS instance. More advanced searches and filters are also possible, such as filtering Objects based on metadata values or numerical threshold.

In this sub-section, we focus on filtering Objects.

Methods such as `get_objects()` typically return all the matching Objects in an instance. For efficiency, it is often better to retrieve results in batches. This can be achieved using the `count` and `start_with` parameters:

```python
start_with = 3 

experimental_steps = o.get_objects(
    type="EXPERIMENTAL_STEP",
    count=6, 
    start_with=start_with,
)
```

Here, `start_with` specifies the index at which the result list starts, while `count` defines how many Objects are returned. The `type` parameter restricts the search to a specific Object type (in this case, `EXPERIMENTAL_STEP`).

```python
for step in experimental_steps:
    print(f"Experimental step: {step.code}")
```

You can also retrieve Objects whose properties match certain values:

```python
o.get_objects(
    where={"$name": "* <name-we-want-to-find>"},
    props=["$name"],
)
```

Here, the `props` parameter ensures that `$name` is included in the returned results.

Mathematical comparison operators (`>`, `<`, `=`, `>=`, `<=`) can also be used:

```python
o.get_objects(registrationdate=">2023-07-21")
```

And even more complex searches:

```python
o.get_objects(
    space="MY_*",  # spaces starting with MY_
    type="*_STEP*",  # objects types containing _STEP
    withParents="*",  # objects having any parents
    withChildren=[
        "/MY_SPACE/MY_PROJECT/MY_COLLECTION/SAMPLE*",
    ],  # objects having children with codes starting with SAMPLE
)
```
