""" Duty tasks """

from duty import duty
from duty.context import Context


@duty
def translations(ctx: Context):
    """ Update translation """

    print(ctx.run('pybabel extract . -o resources/locales/messages.pot'))
    print(ctx.run(
        'pybabel update -i resources/locales/messages.pot -d resources/locales'))
    print(ctx.run('pybabel compile -f -d resources/locales --use-fuzzy'))


@duty
def optimize(ctx: Context):
    """ Optimize images """''

    print(ctx.run('optimize-images .'))


def pylint(ctx: Context):
    """ Lint  code """

    print(ctx.run('pylint .'))
