//! React 
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

//! Bootstrap
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'

import { getPayloadSub } from '../helpers/Auth'

import hero from '../../images/hero-register.jpeg'


const Login = () => {

  const navigate = useNavigate()



  //! State
  const [formFields, setFormFields] = useState({
    email: '',
    password: '',
  })

  const [error, setError] = useState('')

  //! Executions

  const handleChange = (e) => {
    setFormFields({ ...formFields, [e.target.name]: e.target.value })
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const { data } = await axios.post('/api/profile/login/', formFields)
      localStorage.setItem('CRATE-TOKEN', data.token)
      console.log('DATA TOKEN', data.token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.token}`
      const sub = getPayloadSub()
      navigate(`/profile/${sub}`)

    } catch (err) {
      console.log('error', err)
      setError(err.message)
    }

  }

  return (
    <main>
      <Container className='primary-container'>
        <Row className='top-row'>

          <Col xs={0} sm={0} md={0} lg={6} className='d-none d-lg-block left'>
            <div className='img-container'>
              <img alt='record collection' src={hero}></img>
            </div>
          </Col>

          <Col xs={12} sm={12} md={6} lg={6}>
            <Row>
              <Col className='title-container'>
                <h1 className='display-4 text-center'>CRATE</h1>
                <p className='text-center'>Catalogue your collection. Find new music. Get digging.</p>
              </Col>
            </Row>

            <Row>
              <Form onSubmit={handleSubmit} >
                <div className='form-container'>
                  <h2>Login</h2>

                  <Form.Group className='mb-3'>
                    <Form.Control type="email" name="email" placeholder='Email' onChange={handleChange} value={formFields.email} />
                  </Form.Group>

                  <Form.Group className='mb-3'>
                    <Form.Control type="password" name="password" placeholder='Password' onChange={handleChange} value={formFields.password} />
                  </Form.Group>

                  <Button variant='primary' type='submit' className='mb-3'>
                    Login
                  </Button>

                  {error && <p className='text-danger text-center'>{error}</p>}

                </div>

              </Form>

            </Row>



          </Col>
        </Row>


      </Container>
    </main>
  )
}

export default Login