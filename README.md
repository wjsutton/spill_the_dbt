# Spill the dbt :tea:

A series of practical data transformation challenges with dbt, designed to help you get comfortable with dbt and its functionality.

These challenges generally follow the content for the [dbt Analytics Engineer Certification](https://www.getdbt.com/certifications/analytics-engineer-certification-exam), providing hands-on experience with concepts covered in the certification.

## Getting Started

**📺 [Installation walkthrough now available](https://youtu.be/rSI1VcSpXq0)**

To work with these challenges, please follow the steps below:

**1. Fork the Repository**

You should fork the repository to your own GitHub account:

- Click the "Fork" button at the top right corner of this page.
- Choose your GitHub account to fork the repository.

**2. Clone Your Forked Repository**

Once you've forked the repository, clone it to your local machine using:
- [GitHub Desktop](https://desktop.github.com/download/), 
- [VSCode's GitHub extension](https://vscode.github.com/) 
- or the [git](https://git-scm.com/) command below

```
gh repo clone your-username/spill_the_dbt
```

**3. Set Up Your Environment**

- Install Python: Ensure you have [Python](https://www.python.org/) installed on your machine that is compatible with dbt. Check [What version of Python can I use?](https://docs.getdbt.com/docs/core/pip-install)
- Install Required Python Packages, includes dbt-core, you may wish to [run dbt another way](https://docs.getdbt.com/docs/core/installation-overview). 
- Setup your computer for [working on dbt projects](https://discourse.getdbt.com/t/how-we-set-up-our-computers-for-working-on-dbt-projects/243)

**Create a virtual environment**
```
python -m venv dbt-env
```

**Activate your virtual environment**
Windows:
```
dbt-env\Scripts\activate
```
Mac / Linux
```
source dbt-env/bin/activate
```
**Install the required packages**
``` bash
pip install -r requirements.txt
```

**4. Work Through the Challenge**

- Follow the step-by-step instructions provided in the challenge markdown file.
- Write your dbt models, tests, and code as instructed.
- Use Git to commit your changes to your forked repository.

**5. Optional: Share Your Solutions**

If you'd like to share your solutions on social:
- Use the hashtag **#SpillTheDBT** 
- Add an image of your code with [carbon.now.sh/](https://carbon.now.sh/) 
- Write about your solution and the techniques used to complete the challenge

If you'd like to contribute back to the project, you can create a pull request for [spill_the_dbt](https://github.com/wjsutton/spill_the_dbt).


## Challenges

| Week | Challenge         | Estimated Time                                    | Skills Tested | Walkthrough                                             | Solutions                                                |
|----- |-----------------------|------------------------------------------------------|-------|---------------------------------------------------------|----------------------------------------------------------|
| 1. | [Introduction to dbt-core](https://github.com/wjsutton/spill_the_dbt/blob/main/tasks/challenge_01.md) | 1/2 a day      | - Basic connection profiles<br>- Migrating SQL code to dbt<br>- Running and testing models<br>- Referencing model outputs<br>- Generating documentation | [📺 Walkthrough](https://www.youtube.com/watch?v=vERj9AixGCM) | [Solution](https://github.com/wjsutton/spill_the_dbt/tree/solutions/challenge_01) |
| 2. | [Testing models to find errors](https://github.com/wjsutton/spill_the_dbt/blob/main/tasks/challenge_02.md) | 1/2 a day        | - Generic & relationship tests<br>- Custom & singular tests<br>- Tests from dbt packages | Coming soon| [Solution](https://github.com/wjsutton/spill_the_dbt/tree/solutions/challenge_02)
| 3. | [Incremental Models and Python](https://github.com/wjsutton/spill_the_dbt/blob/main/tasks/challenge_03.md) | 1 day        | - Incremental models<br>- Python models<br>- API data integration<br>- Tests from dbt packages | Coming soon| [Solution](https://github.com/wjsutton/spill_the_dbt/tree/solutions/challenge_03)

*More challenges coming soon!*

## Contributing

Contributions are welcome! If you have ideas for new challenges, improvements to existing ones, or want to share your solutions, please feel free to:

- Open an Issue: Use the GitHub Issues tab to discuss your ideas or report problems.
- Create a Pull Request: Fork the repository, make your changes, and submit a pull request for review.

Please ensure your contributions align with the project's goals and that you follow the contribution guidelines.

**Contribution Guidelines**

- Be respectful and considerate in your interactions.
- Avoid offensive or inappropriate language and content.
- Provide constructive feedback and be open to feedback on your contributions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the dbt community for their support and resources.
These challenges are inspired by the content for the dbt Analytics Engineer Certification.
