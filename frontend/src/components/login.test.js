import React from 'react'
import { render, fireEvent, act } from '@testing-library/react'
import Login from './login' // Assuming Login is the export from your file

test('email validation on submit', () => {
  const { getByLabelText, getByText, queryByText } = render(<Login />)

  // Find the inputs and button
  const emailInput = getByLabelText('Email address')
  const submitButton = getByText('Sign in')

  // Submit without entering an email
  act(() => {
    fireEvent.click(submitButton)
  })

  // Expect to see the email error message
  expect(queryByText('Email is required')).toBeInTheDocument()

  // Enter an invalid email
  act(() => {
    fireEvent.change(emailInput, { target: { value: 'invalidemail' } })
    fireEvent.click(submitButton)
  })

  // Expect to see the invalid email error message
  expect(queryByText('Please enter a valid email')).toBeInTheDocument()
})

test('password validation on submit', () => {
  const { getByLabelText, getByText, queryByText } = render(<Login />)

  // Find the inputs and button
  const emailInput = getByLabelText('Email address')
  const passwordInput = getByLabelText('Password')
  const submitButton = getByText('Sign in')

  // Enter a valid email but leave password blank
  act(() => {
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
    fireEvent.click(submitButton)
  })

  // Expect to see the password error message
  expect(queryByText('Password is required')).toBeInTheDocument()
})
