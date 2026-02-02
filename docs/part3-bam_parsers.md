Up to this point, you have learned how to work with pyBIS to explore, create, and search metadata in openBIS. Despite their inmense usefulness, individual pyBIS scripts suffer from maintainability and discoverability issues: **two different people can easily create different pyBIS scripts that implement the same functionality**.

For this reason, and specifically in the context of creating new Objects and defining their relationships (i.e., automated data ingestion in openBIS), the BAM Data Store decided to define a common interface in the [BAM Masterdata](https://github.com/BAMresearch/bam-masterdata) GitHub repository. This interface allows you to create **parser scripts** in a standardized way.

When deciding whether to write a standalone pyBIS script or to use the BAM Parser Infrastructure, you should ask yourself the following questions:

1. Is this script used to read metadata from files that are continously being produced in my laboratory?
2. Is this script going to be used by other people?
3. Does the logic I implemented go beyond my specific use case?

If the answer to all these questions is **yes**, then you should create a parser following the BAM Parser Infrastructure and its documentation. In particular, we recommend starting with:

* [Tutorial: Parsing data using BAM Masterdata](https://bamresearch.github.io/bam-masterdata/tutorials/parsing/).
* [How-to: Create a New Parser](https://bamresearch.github.io/bam-masterdata/howtos/parsing/create_new_parsers/).

For a deeper understanding, you can also read:

* [Explanation: Parsing and ETL Structure in the Parser App](https://bamresearch.github.io/bam-masterdata/explanations/parsing_structure/).

??? question "Why use this instead of pyBIS directly?"
    Beyond the issue of duplicated scripts, the BAM Parser Infrastructure allows you to focus primarily on parsing and structuring metadata for Objects, rather than on repeatedly implementing connection logic, authentication, error handling, and object creation workflows.
    In the future, we plan to deploy a dedicated [Parser App](https://bamresearch.github.io/bam-masterdata/howtos/parsing/parser_app/) that will load and execute these parsers through a user-friendly interface. Parsers that do not follow the BAM Parser Infrastructure will **not** be integrable into this application.