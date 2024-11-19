# Contributing

Contributions to this repository are welcome and much appreciated.

## Submitting changes

Contributions can be provided as [pull requests][prs] to this extension's
GitHub project. New contributors should familiarize themselves with the
following:

- **(required)** Sign your work ([Developer’s Certificate of Origin][dcod]).
  This is confirmed with the inclusion of `Signed-off-by` in submitted
  commit messages.
- Builds are required\* to pass to be accepted (\* with some exceptions
  in very specific scenarios). When a pull request is submitted, continuous
  integration tests will be invoked. A developer can invoke `tox` at the
  root of the checked out repository to validate changes before submitting
  a pull request.
- Keep a narrow scope for proposed changes. Submitting multiple feature
  changes in a single pull request is not always helpful. Use multiple
  commits to separate changes over stacking all changes in a single commit
  (for example, related implementation and documentation changes can be
  submitted in a single pull request, but are best presented in their own
  individual commits).
- Add unit tests (if applicable). Adding unit tests to validate new changes
  helps build confidence for the new modifications and helps prevent future
  changes from breaking the new feature/fix.

While maintainers will help strive to review, merge changes and provide
support (when possible), the process may take some time. Please be patient
and happy coding.

## Guidelines

A goal of this utility is to include support for all stable Python
interpreters that have yet to be marked as [end-of-life][python-eol].

[PEP 8][pep8] is a standard styling guide for Python projects and is
recommended for consideration when making contributions. Default linters
configured in tox are required to pass. Note that select exceptions may
be used.


[dcod]: https://developercertificate.org/
[issues]: https://github.com/jdknight/pybadges2/issues
[pep8]: https://peps.python.org/pep-0008/
[prs]: https://github.com/jdknight/pybadges2/pulls
[python-eol]: https://devguide.python.org/versions/
