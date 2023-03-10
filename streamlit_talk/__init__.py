import os
import time
from typing import Literal, Optional, Union

import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True
COMPONENT_NAME = "streamlit_talk"

if _RELEASE:  # use the build instead of development if release is true
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/build")

    _streamlit_talk = components.declare_component(COMPONENT_NAME, path=build_dir)
else:
    _streamlit_talk = components.declare_component(
        COMPONENT_NAME, url="http://localhost:3000"
    )

# data type for avatar style
AvatarStyle = Literal[
    "adventurer",
    "adventurer-neutral",
    "avataaars",
    "big-ears",
    "big-ears-neutral",
    "big-smile",
    "bottts",
    "croodles",
    "croodles-neutral",
    "female",
    "gridy",
    "human",
    "identicon",
    "initials",
    "jdenticon",
    "male",
    "micah",
    "miniavs",
    "pixel-art",
    "pixel-art-neutral",
    "personas",
]

@st.cache_resource(experimental_allow_widgets=True)
def message(
    value: str,
    animate_from: str = "",
    is_user: Optional[bool] = False,
    avatar_style: Optional[AvatarStyle] = None,
    seed: Optional[Union[int, str]] = 42,
    key: Optional[str] = None,
    use_typewriter: bool = False,
    partial_replies: bool = False,
    generation_complete: bool = True,
):
    """
    Creates a new instance of streamlit-chat component

    Parameters
    ----------
    message: str
        The message to be displayed in the component
    is_user: bool
        if the sender of the message is user, if `True` will align the
        message to right, default is False.
    avatar_style: Literal or None
        The style for the avatar of the sender of message, default is bottts
        for not user, and pixel-art-neutral for user.
        st-chat uses https://avatars.dicebear.com/styles for the avatar
    seed: int or str
        The seed for choosing the avatar to be used, default is 42.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns: None
    """
    if not avatar_style:
        avatar_style = "pixel-art-neutral" if is_user else "bottts"

    if not partial_replies:
        return _streamlit_talk(
            value=value,
            animateFrom=animate_from,
            seed=seed,
            isUser=is_user,
            avatarStyle=avatar_style,
            key=key,
            useTypewriter=use_typewriter,
            default=True,
            partialReplies=partial_replies,
            generationComplete=generation_complete,
        )
    else:
        if st.session_state.get("force_animation", None):
            return_value = _streamlit_talk(
                value=value,
                animateFrom=animate_from,
                seed=seed,
                isUser=is_user,
                avatarStyle=avatar_style,
                key=None,
                useTypewriter=True,
                default=True,
                partialReplies=partial_replies,
                generationComplete=generation_complete,
            )
            if return_value != False:
                st.session_state.force_animation = False
                # the typewriter animation will force a refresh
                st.stop()

        else:
            return _streamlit_talk(
                value=value,
                animateFrom=animate_from,
                seed=seed,
                isUser=is_user,
                avatarStyle=avatar_style,
                key=key,
                useTypewriter=False,
                default=True,
                partialReplies=partial_replies,
                generationComplete=generation_complete,
            )


if not _RELEASE:
    import streamlit as st

    chatlog_placeholder = st.empty()
    user_input_placeholder = st.empty()
    persona_selection_placeholder = st.empty()

    # testing
    long_message = """A chatbot or chatterbot is a software application used to conduct an on-line chat conversation via text or text-to-speech, in lieu of providing direct contact with a live human agent.\n\nDesigned to convincingly simulate the way a human would behave as a conversational partner, chatbot systems typically require continuous tuning and testing, and many in production remain unable to adequately converse, while none of them can pass the standard Turing test. The term "ChatterBot" was originally coined by Michael Mauldin (creator of the first Verbot) in 1994 to describe these conversational programs.
    """
    user_avatar = (
        "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/1f464.png"
    )
    bot_avatar = (
        "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/1f1ec-1f1f7.png"
    )

    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def partial_replies():
        replies = [
            "Hello, I am a Chatbot, how may I help you? I can help you with all sorts of things!",
        ]
        for i in range(5):
            replies.append(
                f"{replies[-1]}\n\nThis is A chatbot or chatterbot {i}"
            )
        for reply in replies:
            time.sleep(6)
            yield reply

    def peek(iterable) -> str:
        """Retrieves the next item from a generator object if it exists.

        Args:
            iterable (generator): A partial reply generator

        Returns:
            str: Returns the next partial reply
        """
        try:
            first = next(iterable)
        except StopIteration:
            return ""
        return first

    def render_message():
        st.session_state.message_submitted = True
        st.session_state.prev_message = "Hello, I am a Chatbot,"
        st.session_state.replies = partial_replies()
        st.session_state.curr_message = next(st.session_state.replies)
        st.session_state.force_animation = True
        st.session_state.start_loop = True
        st.session_state.rerun_counter = 0
        st.session_state.generation_complete = False

    message(long_message, avatar_style=bot_avatar)
    message("Hey, what's a chatbot?", is_user=True, avatar_style=user_avatar)
    message(
        value="hi there",
        animate_from="hi there",
        use_typewriter=True,
        generation_complete=True
    )
    if st.session_state.get("message_submitted"):
        message(
            value=st.session_state.curr_message,
            animate_from=st.session_state.prev_message,
            use_typewriter=True,
            key="last_message_animation",
            generation_complete=st.session_state.generation_complete
        )

    def change_message_state(new_message):
        st.session_state.force_animation = True
        st.session_state.prev_message = st.session_state.curr_message
        st.session_state.curr_message = new_message

    if "replies" in st.session_state:
        curr_reply = peek(st.session_state.replies)
        if curr_reply != "":
            change_message_state(new_message=curr_reply)
            st.experimental_rerun()
        else:
            del st.session_state.replies
            st.session_state.generation_complete = True
            st.experimental_rerun()

    st.button("Message:", on_click=render_message())
