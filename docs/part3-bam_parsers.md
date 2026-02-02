Up until now, you've learned how to work with pyBIS to explore, create, and search metainformation in openBIS. Despite of their inmense help, individual pyBIS scripts suffer from a maintainability and findability issue: two different people can create different pyBIS scripts with the same functionality. That's why, in the context of creating new Objects and their relationships (i.e., automated data ingestion in openBIS), we decided to create an interface (defined in the [BAM Masterdata](https://github.com/BAMresearch/bam-masterdata) GitHub repository), and offer you with the opportunity to create **parser** scripts in a standardize way.

When making a decision if writing a Python script in pyBIS or with this infrastructure, you should ask yourself:

1. Is this script used for reading metadata from files that are constantly produced in my laboratory?
2. Is this script going to be used by others?
3. Did I create logic that might not be specific to my script?

If the answer to all this questions is "yes", then you should create a parser following the BAM Parser Infrastructure and documentation. We recommend following:

* [A tutorial on how to parse data using BAM Masterdata](https://bamresearch.github.io/bam-masterdata/tutorials/parsing/)
* [How-to: Create a New Parser](https://bamresearch.github.io/bam-masterdata/howtos/parsing/create_new_parsers/)

If you want to know more, you can read our [Explanation: Parsing and ETL Structure in the Parser App](https://bamresearch.github.io/bam-masterdata/explanations/parsing_structure/).

!!! question Why using this instead of pyBIS directly?
    Besides the multiplicity issue, the BAM Parser Infrastructure allows you to quickly focus on parsing metadata of Objects, and not on connecting to openBIS, creating custom logic, etc. In a future, we are planning to deploy our own [Parser App](https://bamresearch.github.io/bam-masterdata/howtos/parsing/parser_app/) which will load these parsers into it to produce an easy-to-follow interface for other users. If your script does not follow the BAM Parser Infrastructure, then it won't be integrated in such app.
