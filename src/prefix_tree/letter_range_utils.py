from typing import (
    List,
)

_SQUARE_BRACKET_ESCAPABLES = {'[', ']', '\\'}


def escape_char_in_square_brackets(character: str) -> str:
    return '\\' + character if character in _SQUARE_BRACKET_ESCAPABLES else character


def _formatted_letter_range(first_letter: str, last_letter: str) -> List[str]:
    if first_letter == last_letter:
        raise RuntimeError(
            "first_letter and last_letter must not be the same."
        )  # pragma: no cover

    if ord(first_letter) + 1 < ord(last_letter):
        return [first_letter + '-' + last_letter]

    return [first_letter, last_letter]


def _is_next_letter(first_letter: str, second_letter: str) -> bool:
    return ord(first_letter) + 1 == ord(second_letter)


_STATE_NO_RANGE = 1
_STATE_RANGE_START = 2
_STATE_IN_RANGE = 3


# TODO(Radek): Implement proper FSM
def collapse_letter_ranges(  # pylint: disable=too-many-branches; required for FSM implementation
        letters: List[str]
) -> List[str]:
    if len(letters) == 1:
        return [escape_char_in_square_brackets(letters[0])]

    # Make hyphen first in the list, if present
    letters.sort(key=lambda character: -1 if character == '-' else ord(character))
    letters_out = []  # type: List[str]
    state = _STATE_NO_RANGE
    first_letter = ''
    previous_letter = ''
    last_index = len(letters)

    for index, current_letter in enumerate(letters, 1):
        if state == _STATE_NO_RANGE:
            if current_letter.isalnum():
                state = _STATE_RANGE_START
                first_letter = current_letter
            else:
                letters_out.append(escape_char_in_square_brackets(current_letter))

        elif state == _STATE_RANGE_START:
            if not current_letter.isalnum():
                state = _STATE_NO_RANGE
                letters_out.append(first_letter)
                letters_out.append(escape_char_in_square_brackets(current_letter))
            elif _is_next_letter(previous_letter, current_letter):
                state = _STATE_IN_RANGE
            else:
                letters_out.append(first_letter)
                first_letter = current_letter

        elif state == _STATE_IN_RANGE:
            if not _is_next_letter(previous_letter, current_letter):
                state = _STATE_RANGE_START
                letters_out.extend(_formatted_letter_range(first_letter, previous_letter))
                first_letter = current_letter
        else:
            raise RuntimeError("Unexpected state: " + str(state))  # pragma: no cover

        if index == last_index:
            if state == _STATE_RANGE_START:
                letters_out.append(current_letter)
            elif state == _STATE_IN_RANGE:
                letters_out.extend(_formatted_letter_range(first_letter, current_letter))

        previous_letter = current_letter

    return letters_out
