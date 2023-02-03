import {
  // eslint-disable-next-line 
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ComponentProps, useEffect, useState } from "react"
import styled from '@emotion/styled'
import { css } from '@emotion/react'
import Typewriter from 'typewriter-effect'


// custom callback to refresh streamlit on every character typed
const refreshStreamlitAndCreateNode = (character: string) => {
  Streamlit.setFrameHeight();
  return document.createTextNode(character)
}

const MessageContainer = (props: ComponentProps<any>) => {
  const { theme, value, animateFrom, useTypewriter } = props
  const StyledDiv = styled.div({
    display: 'inline-block',
    background: theme.secondaryBackgroundColor,
    border: '1px solid transparent',
    borderRadius: '10px',
    padding: '10px 14px',
    margin: '5px 20px',
    maxWidth: '70%',
    whiteSpace: 'pre-wrap',
  })
  if (useTypewriter) {
    console.log("rendering with typewriter")
    return (
      <StyledDiv>
        <Typewriter
          options={{
            delay: 10,
            cursor: '▎',
            onCreateTextNode: refreshStreamlitAndCreateNode
          }}
          onInit={typewriter => {
            typewriter
              .pasteString(animateFrom, null)
              .typeString(
                value.split(animateFrom).join('')
              )
              .callFunction(state => {
                setTimeout(() => state.elements.cursor.setAttribute('hidden', 'hidden'), 3500)
                typewriter.stop()
                Streamlit.setComponentValue(false);
              })
              .start()
          }}
        />
      </StyledDiv>
    )
  } else {
    return (
      <StyledDiv>
        {value}
      </StyledDiv>
    )
  }
}

const Chat = (props: ComponentProps<any>) => {
  useEffect(() => {
      Streamlit.setFrameHeight()
    }
  );
  const { isUser, avatarStyle, seed, animateFrom, value, useTypewriter } = props.args

  let avatarUrl
  if (avatarStyle.startsWith("https")) {
    avatarUrl = avatarStyle
  } else if (avatarStyle.startsWith("data:image")) {
    avatarUrl = avatarStyle
  } else {
    avatarUrl = `https://avatars.dicebear.com/api/${avatarStyle}/${seed}.svg`
  }

  // Streamlit sends us a theme object via props that we can use to ensure
  // that our component has visuals that match the active theme in a
  // streamlit app.
  const { theme } = props
  // Maintain compatibility with older versions of Streamlit that don't send
  // a theme object.
  if (!theme) {
    return <div>Theme is undefined, please check streamlit version.</div>
  }

  // styles for the avatar image
  const Avatar = styled.img({
    border: `1px solid transparent`,
    // borderRadius: '50%',
    height: '3rem',
    width: '3rem',
    margin: 0,
  })

  // styles for the container
  const ChatContainer = styled.div({
    display: 'flex',
    // flexDirection: 'row',
    fontFamily: `${theme.font}, 'Segoe UI', 'Roboto', sans-serif`, 
    height: 'auto',
    margin: 0,
    width: '100%'
  }, 
  (props: {isUser: boolean}) => {  // specific styles
    if (props.isUser){
      return css`
        flex-direction: row-reverse;
        & > div {
          text-align: right;
        }
        padding-right: 5px;
      `
    }
    return css``
  })
  
  // custom callback to refresh streamlit on every character typed
  const refreshStreamlitAndCreateNode = (character: string) => {
    Streamlit.setFrameHeight()
    return document.createTextNode(character)
  }
  if (!isUser) {
    return (
      <ChatContainer isUser={isUser}>
        <Avatar src={avatarUrl} alt="profile" draggable="false"/>
        <MessageContainer theme={theme} value={value} animateFrom={animateFrom} useTypewriter={useTypewriter}>
        </MessageContainer>
      </ChatContainer>
    )
  } else {
    return (
      <ChatContainer isUser={isUser}>
        <Avatar src={avatarUrl} alt="profile" draggable="false"/>
        <MessageContainer theme={theme} value={value} animateFrom={animateFrom}>
        </MessageContainer>
      </ChatContainer>
    )
  }
} 

export default withStreamlitConnection(Chat);
