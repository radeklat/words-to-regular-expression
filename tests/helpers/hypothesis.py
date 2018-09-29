from hypothesis import strategies as st


NON_EMPTY_STRINGS = st.characters().filter(lambda _: _.strip())


NON_EMPTY_TEXT_ITERABLES = st.lists(
    NON_EMPTY_STRINGS, min_size=1, max_size=100
)

LISTS_OF_WORDS = st.lists(
    st.builds(
        lambda _: ''.join(_),
        st.lists(st.characters(whitelist_categories=(
            'Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nd', 'Nl', 'No'
        )), min_size=1),
    ),
    min_size=1, max_size=100
)

NON_ALPHANUMERIC_STRING = st.builds(
    lambda _: ''.join(_),
    st.lists(st.characters(whitelist_categories=(
        'Zs', 'Zl', 'Zp'
    )), min_size=1),
)

SPECIAL_CHARACTER_STRINGS = {
    '*': '\*',
    '***': '[\*]{3}',
    '+': '\+',
    '{': '\{',
    '}': '\}',
    '{}': '\{\}',
    '{1}': '\{1\}',
    '{1,3}': '\{1\,3\}',
    '++': '[\+]{2}',
    '...': '[\.]{3}',
    '.': '\.',
    '?': '\?',
    '???': '[\?]{3}',
    '[': '\[',
    ']': '\]',
    '[]': '\[\]',
    '-': '\-',
}
