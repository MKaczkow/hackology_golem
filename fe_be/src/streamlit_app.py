import asyncio
import os
from collections.abc import AsyncGenerator

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

from client import AgentClient
from schema import ChatMessage
import pandas as pd
from io import StringIO

# A Streamlit app for interacting with the langgraph agent via a simple chat interface.
# The app has three main functions which are all run async:

# - main() - sets up the streamlit app and high level structure
# - draw_messages() - draws a set of chat messages - either replaying existing messages
#   or streaming new ones.
# - handle_feedback() - Draws a feedback widget and records feedback from the user.

# The app heavily uses AgentClient to interact with the agent's FastAPI endpoints.


APP_TITLE = "Agent Service Toolkit"
APP_ICON = "🧰"


@st.cache_resource
def get_agent_client() -> AgentClient:
    agent_url = os.getenv("AGENT_URL", "http://localhost")
    return AgentClient(agent_url)


async def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        menu_items={},
    )

    # Hide the streamlit upper-right chrome
    st.html(
        """
        <style>
        [data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
            }
        </style>
        """,
    )
    if st.get_option("client.toolbarMode") != "minimal":
        st.set_option("client.toolbarMode", "minimal")
        await asyncio.sleep(0.1)
        st.rerun()

    models = {
        "OpenAI GPT-4o-mini (streaming)": "gpt-4o-mini",
        "Gemini 1.5 Flash (streaming)": "gemini-1.5-flash",
        "Claude 3 Haiku (streaming)": "claude-3-haiku",
        "llama-3.1-70b on Groq": "llama-3.1-70b",
    }
    # Config options
    with st.sidebar:
        st.header(f"{APP_ICON} {APP_TITLE}")
        ""
        "Full toolkit for running an AI agent service built with LangGraph, FastAPI and Streamlit"
        with st.popover(":material/settings: Settings", use_container_width=True):
            m = st.radio("LLM to use", options=models.keys())
            model = models[m]
            use_streaming = st.toggle("Stream results", value=True)

        @st.dialog("Architecture")
        def architecture_dialog() -> None:
            st.image(
                "https://github.com/JoshuaC215/agent-service-toolkit/blob/main/media/agent_architecture.png?raw=true"
            )
            "[View full size on Github](https://github.com/JoshuaC215/agent-service-toolkit/blob/main/media/agent_architecture.png)"
            st.caption(
                "App hosted on [Streamlit Cloud](https://share.streamlit.io/) with FastAPI service running in [Azure](https://learn.microsoft.com/en-us/azure/app-service/)"
            )

        if st.button(":material/schema: Architecture", use_container_width=True):
            architecture_dialog()

        with st.popover(":material/policy: Privacy", use_container_width=True):
            st.write(
                "Prompts, responses and feedback in this app are anonymously recorded and saved to LangSmith for product evaluation and improvement purposes only."
            )

        "[View the source code](https://github.com/JoshuaC215/agent-service-toolkit)"
        st.caption(
            "Made with :material/favorite: by [Joshua](https://www.linkedin.com/in/joshua-k-carroll/) in Oakland"
        )

    # Draw existing messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    messages: list[ChatMessage] = st.session_state.messages

    if len(messages) == 0:
        WELCOME = "Cześć jestem asystentem sprzedawcy w czym mogę pomóc?"
        with st.chat_message("ai"):
            st.write(WELCOME)

    # draw_messages() expects an async iterator over messages
    async def amessage_iter() -> AsyncGenerator[ChatMessage, None]:
        for m in messages:
            yield m

    await draw_messages(amessage_iter())

    # Generate new message if the user provided new input
    if user_input := st.chat_input():
        messages.append(ChatMessage(type="human", content=user_input))
        st.chat_message("human").write(user_input)
        agent_client = get_agent_client()
        if use_streaming:
            stream = agent_client.astream(
                message=user_input,
                model=model,
                thread_id=get_script_run_ctx().session_id,
            )
            await draw_messages(stream, is_new=True)
        else:
            response = await agent_client.ainvoke(
                message=user_input,
                model=model,
                thread_id=get_script_run_ctx().session_id,
            )
            messages.append(response)
            st.chat_message("ai").write(response.content)
        st.rerun()  # Clear stale containers

    # If messages have been generated, show feedback widget
    if len(messages) > 0:
        with st.session_state.last_message:
            await handle_feedback()


async def draw_messages(
    messages_agen: AsyncGenerator[ChatMessage | str, None],
    is_new: bool = False,
) -> None:
    """
    Draws a set of chat messages - either replaying existing messages
    or streaming new ones.

    This function has additional logic to handle streaming tokens and tool calls.
    - Use a placeholder container to render streaming tokens as they arrive.
    - Use a status container to render tool calls. Track the tool inputs and outputs
      and update the status container accordingly.

    The function also needs to track the last message container in session state
    since later messages can draw to the same container. This is also used for
    drawing the feedback widget in the latest chat message.

    Args:
        messages_aiter: An async iterator over messages to draw.
        is_new: Whether the messages are new or not.
    """

    # Keep track of the last message container
    last_message_type = None
    st.session_state.last_message = None

    # Placeholder for intermediate streaming tokens
    streaming_content = ""
    streaming_placeholder = None

    # Iterate over the messages and draw them
    while msg := await anext(messages_agen, None):
        # str message represents an intermediate token being streamed
        if isinstance(msg, str):
            # If placeholder is empty, this is the first token of a new message
            # being streamed. We need to do setup.
            if not streaming_placeholder:
                if last_message_type != "ai":
                    last_message_type = "ai"
                    st.session_state.last_message = st.chat_message("ai")
                with st.session_state.last_message:
                    streaming_placeholder = st.empty()

            streaming_content += msg
            streaming_placeholder.write(streaming_content)
            continue
        if not isinstance(msg, ChatMessage):
            st.error(f"Unexpected message type: {type(msg)}")
            st.write(msg)
            st.stop()
        match msg.type:
            # A message from the user, the easiest case
            case "human":
                last_message_type = "human"
                st.chat_message("human").write(msg.content)

            # A message from the agent is the most complex case, since we need to
            # handle streaming tokens and tool calls.
            case "ai":
                # If we're rendering new messages, store the message in session state
                if is_new:
                    st.session_state.messages.append(msg)

                # If the last message type was not AI, create a new chat message
                if last_message_type != "ai":
                    last_message_type = "ai"
                    st.session_state.last_message = st.chat_message("ai")

                with st.session_state.last_message:
                    # If the message has content, write it out.
                    # Reset the streaming variables to prepare for the next message.
                    if msg.content:
                        if streaming_placeholder:
                            streaming_placeholder.write(msg.content)
                            streaming_content = ""
                            streaming_placeholder = None
                        else:
                            st.write(msg.content)

                    if msg.tool_calls:
                        # Create a status container for each tool call and store the
                        # status container by ID to ensure results are mapped to the
                        # correct status container.
                        call_results = {}
                        for tool_call in msg.tool_calls:
                            status = st.status(
                                f"""Tool Call: {tool_call["name"]}""",
                                state="running" if is_new else "complete",
                            )
                            call_results[tool_call["id"]] = status
                            status.write("Input:")
                            status.write(tool_call["args"])

                        # Expect one ToolMessage for each tool call.
                        for _ in range(len(call_results)):
                            tool_result: ChatMessage = await anext(messages_agen)
                            if tool_result.type != "tool":
                                st.error(f"Unexpected ChatMessage type: {tool_result.type}")
                                st.write(tool_result)
                                st.stop()

                            # Record the message if it's new, and update the correct
                            # status container with the result
                            if is_new:
                                st.session_state.messages.append(tool_result)
                            status = call_results[tool_result.tool_call_id]
                            status.write("Output:")
                            status.write(tool_result.content)
                            if "prediction" in tool_result.content:
                                # df = pd.read_csv("src/prediction.csv")
                                csv_data = """
Date,Max,Avg,Min
2000-09-17,-0.3623783508164823,-0.4456854815725732,-0.6085149853565455
2000-09-18,-0.2363507485082679,-0.4048926175879082,-0.9562848383362704
2000-09-19,0.4682511750807943,0.25251762209816603,-0.3314041023881524
2000-09-20,0.4634433946088658,0.045220888804010075,-0.8521502653168315
2000-09-21,0.8847072116321316,0.8336182705078664,0.730921568659702
2000-09-22,0.5918053543582634,0.12952170134353,-0.6232256896016344
2000-09-23,1.0306636640235851,0.9544565260847647,0.8620496820042491
2000-09-24,0.9617543138605008,0.9072354702902277,0.785974987617701
2000-09-25,0.9611905027098608,0.6699065529147363,0.3341431507257955
2000-09-26,1.1778489028742771,0.5873850364062967,-0.1779512814229829
2000-09-27,0.8648564220186218,0.5864460641137293,0.2668525849789623
2000-09-28,0.5741303878231951,0.38947328536982434,0.208041638805064
2000-09-29,0.3928931241067674,0.08491773148651094,-0.3368838001917761
2000-09-30,0.2861798943567432,-0.14982481962587105,-0.9567380858012058
2000-10-01,-0.1686918266528016,-0.4912720224777654,-0.7757670896237598
2000-10-02,-0.0344529055804527,-0.4205126777095345,-1.1709932743419995
2000-10-03,1.1092305376371443,-0.1427077279215496,-1.036180494083529
2000-10-04,0.5831836729672847,-0.3560664497645931,-0.990185539759777
2000-10-05,-0.2977252452215893,-0.4481863475451968,-0.7202837389022283
2000-10-06,0.1251397505068896,-0.25727980623203345,-0.8967265212242779
2000-10-07,-0.1221359926488185,-0.5212020836486563,-1.037881891326529
2000-10-08,0.1275358739581503,-0.2237824274607021,-0.5300339514792215
2000-10-09,0.6813794852225423,0.11485482479844626,-0.317857542387121
2000-10-10,0.671835293191625,0.35904100573216097,-0.0223498744687669
2000-10-11,0.8974224789634023,0.5559998496768229,0.0164939389990401
2000-10-12,0.8745029460885776,0.5399643079253412,-0.0089572980426315
2000-10-13,1.0004763226176214,0.5690038406792559,-0.601739614990454
2000-10-14,0.983338438414755,0.6399091939028115,-0.078529757192824
2000-10-15,0.8557218822064537,0.40691999006098684,-0.626463151454821
2000-10-16,0.8000127532732708,0.46321292546158316,-0.195383578477483
2000-10-17,0.9844108105572348,0.5457404364220386,0.1644445946474424
2000-10-18,1.2506483793258667,0.3053166450270312,-1.4062864780426023
2000-10-19,0.3094594724674158,0.03358958895061531,-0.3106367543461369
2000-10-20,0.3947709742511821,-0.3792458339420768,-1.258955457159391
2000-10-21,1.2506483793258667,0.19662595206422032,-0.6078700663968565
2000-10-22,0.2753575800960678,-0.16123819330165554,-0.7352997156124585
2000-10-23,0.72862838929278,-0.2522675232045523,-0.9804515787785832
2000-10-24,0.9424646767080884,-0.15737251989141496,-1.0122052065296243
2000-10-25,-0.214806494737524,-0.4542227060338002,-1.406345009803772
2000-10-26,0.405756644943414,-0.3194165598934473,-0.9758604533020268
2000-10-27,1.1406079530715942,0.24030440380563234,-0.6581193824127116
2000-10-28,0.4283365799665577,-0.036600835078488804,-0.5782841440502894
2000-10-29,0.9977120088701372,0.41991052958447206,-0.327360541805491
2000-10-30,0.8349006446461769,0.6383047058368847,0.1882262745201342
2000-10-31,1.0484092394565003,0.448082209390063,-0.4661595914263927
2000-11-01,0.7584658253596828,0.5375318420903081,0.0060804048229204
2000-11-02,1.0225437309476268,0.6483311272828146,0.12895353205285
2000-11-03,0.9341732863616224,0.5044336247425399,-0.4089023207677245
2000-11-04,0.8381876055437473,0.5092528319020023,0.0759179297671595
2000-11-05,1.201245513458017,0.37743302201961876,-1.2409482823038132
2000-11-06,0.6691651381577582,0.1506756565356495,-0.7809334590321647
2000-11-07,0.5950627399867919,0.06020702727982249,-0.8066698688251067
2000-11-08,0.3297551834275554,-0.17146685766901162,-0.9908949043931402
2000-11-09,0.0622260864421392,-0.4505578632306993,-0.9662666049406428
2000-11-10,-0.092637462616696,-0.5093830038261484,-1.027032318594271
2000-11-11,0.9403295145647774,-0.08320358518642967,-0.985867388650807
2000-11-12,-0.2021014577443269,-0.49473985483489163,-1.1464077747329728
2000-11-13,0.3017179526364952,-0.2660518425861047,-0.6104312605700896
2000-11-14,0.4503289198795948,-0.13895191049005062,-0.558805011029037
2000-11-15,1.0527597408697655,0.12671713938139673,-0.7424343659414888
2000-11-16,0.8755248650140252,0.2659414928045581,-0.869010794271806
2000-11-17,1.1765174437883616,0.42679703945287084,-0.5322010274537093
2000-11-18,1.1075689287210997,0.6617264711900693,-0.2765310442815807
2000-11-19,1.1702962771646463,0.835142564197823,-0.0833736007583134
2000-11-20,1.2506483793258667,0.7415865990558407,-0.06926860080833
2000-11-21,0.9588910077299116,0.6469551878857288,0.0786361153216235
2000-11-22,1.069518312997226,0.6313678888909529,-0.6446224599590977
2000-11-23,1.1141132343025255,0.4353866393382806,-0.4028869870753044
2000-11-24,1.0028526585754602,0.02813983571734217,-1.4062864780426023
2000-11-25,0.9638109193134448,0.2064761649628477,-0.8327834234933559
2000-11-26,0.3625968888043155,-0.16675191609823328,-0.8548547068349149
2000-11-27,0.2326344112525616,-0.35528156967179547,-1.0270830509893638
2000-11-28,-0.4151203562595044,-0.8322096501777642,-1.3688070091444304
2000-11-29,-0.2741623764050644,-0.692469917492211,-1.033501367450785
2000-11-30,-0.2784838113504106,-0.5395265314089711,-1.0381177123562724
2000-12-01,-0.1024142798120279,-0.507373794377261,-1.0410967256817396
2000-12-02,0.4448593641659857,-0.21437862612212952,-0.6663467088532027
2000-12-03,1.114611005791804,0.17732405623571826,-1.0504478740419478
2000-12-04,0.6914364337793888,0.013570840702912737,-0.5337338471722385
2000-12-05,0.6515761039828517,-0.10188442491002815,-1.2033328959756544
"""

                                # Use StringIO to simulate reading from a file
                                csv_io = StringIO(csv_data)

                                # Read the CSV data into a pandas DataFrame
                                df = pd.read_csv(csv_io)
                                st.line_chart(df, x="Date")
                            elif "explanation" in tool_result.content:
                                keys = [
                                    'target_lag-1',
                                    'target_lag-2',
                                    'target_lag-3',
                                    'target_lag-4',
                                    'target_lag-5',
                                    'target_lag-6',
                                    'target_lag-7',
                                    'target_lag-8',
                                    'target_lag-9',
                                    'target_lag-10',
                                    'futcov_lag1',
                                    'futcov_lag2',
                                    'futcov_lag3'
                                ]
                                values = [
                                    0.052, 0.067, 0.113, 0.081, 0.143,
                                    0.064, 0.072, 0.073, 0.115, 0.056,
                                    0.112, 0., 0.052
                                ]
                                df = pd.DataFrame(
                                    {"importances": values}, index=keys
                                )
                                st.bar_chart(df, x_label="Feature name", y_label="Relative feature importance")
                            status.update(state="complete")

            # In case of an unexpected message type, log an error and stop
            case _:
                st.error(f"Unexpected ChatMessage type: {msg.type}")
                st.write(msg)
                st.stop()


async def handle_feedback() -> None:
    """Draws a feedback widget and records feedback from the user."""

    # Keep track of last feedback sent to avoid sending duplicates
    if "last_feedback" not in st.session_state:
        st.session_state.last_feedback = (None, None)

    latest_run_id = st.session_state.messages[-1].run_id
    feedback = st.feedback("stars", key=latest_run_id)

    # If the feedback value or run ID has changed, send a new feedback record
    if feedback is not None and (latest_run_id, feedback) != st.session_state.last_feedback:
        # Normalize the feedback value (an index) to a score between 0 and 1
        normalized_score = (feedback + 1) / 5.0

        agent_client = get_agent_client()
        await agent_client.acreate_feedback(
            run_id=latest_run_id,
            key="human-feedback-stars",
            score=normalized_score,
            kwargs={"comment": "In-line human feedback"},
        )
        st.session_state.last_feedback = (latest_run_id, feedback)
        st.toast("Feedback recorded", icon=":material/reviews:")


if __name__ == "__main__":
    asyncio.run(main())
