# Contributing to champlates

## Copyright and Management

The original author, Hermann Krumrey, has the absolute authority on the
management of this project and may steer the development
process as he sees fit.

Contributions will be attributed to the respective author of said code and the
copyright will remain the author's.

## Coding guidelines

**Unit Testing**

Code should be unit tested with a near-100% coverage. This may not always be
completely feasible, but at least 90%+ should be targeted. However, Unit tests
should not just be done to achieve a high test coverage, writing useful tests
is even more important, just not as easily measurable. Unit tests should be
written using phpunit.

**Style**

We feel that a unified coding style is important, which is why we require a
linter to be used. In this case **phpcheckstyle** is used. The integrated
phpcheckstyle in .checkstyle should be used. As a convenience, lint.sh
can also be used.

In this project, we use tabs for indentation and use a maximum line length of
80 characters (assuming tab characters 4 spaces wide).

**Documentation**

All classes, methods and functions should be described using DocBlock comments.
docstring

Hard to understand parts of code within a method or function should always be
commented accordingly.

## Contributing

All active development is done on a
[self-hosted Gitlab server](https://gitlab.namibsun.net).
To contribute, send an email to hermann@krumreyh.com to create an account.
Once you have an account, you may issue a merge/pull request.

Using the Gitlab issue tracker is preferred, but the issues on Github are also
taken into consideration.
