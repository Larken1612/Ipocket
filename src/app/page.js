'use client'

import { toast, Toaster } from 'react-hot-toast'
import React, { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch, faArrowUp } from '@fortawesome/free-solid-svg-icons'
import { infor } from '../../information.js'
import classNames from 'classnames'

export default function Home() {
  const [scrollVisible, setScrollVisible] = useState(false)
  const [request, setRequest] = useState('')
  const [title, setTitle] = useState('')

  const dataPromise = async (inputData) => {
    const response = await fetch('http://localhost:8000/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(inputData)
    })

    setTitle(`Top 4 ${request}`)
    setRequest('')
    return response
  }
  
  const handleSearch = async (event) => {
    if (request) {
      if (event.key === 'Enter' || event.type === 'click') {
        try {
          const inputData = { 'top': 4, 'request': request }

          toast.promise(dataPromise(inputData), {
            loading: 'Me thinking... 🤔',
            success: 'Me done thinking ⭐',
            error: 'Lỗi khi điều chỉnh dữ liệu 🆘',
          })
        } catch (error) {
          setRequest('')
          toast.error('Có lỗi xảy ra với mô hình của OpenAI 😱')
          setInterval(toast.dismiss(), 3000)
        }
      }
    }
  }

  const arrowClass = 'fixed bottom-4 right-4 float-right cursor-pointer text-4xl bd-0 text-customSearchColorHovered hover:text-customArrowColor hover:-translate-y-2 transition-all ease-in-out duration-400'

  const newArrowClass = classNames(arrowClass, {
    inline: scrollVisible,
    hidden: !scrollVisible
  })

  const toggleVisible = () => {
    const scrolled = document.documentElement.scrollTop
    if (scrolled > 1500) {
      setScrollVisible(true)
    } else {
      setScrollVisible(false)
    }
  }

  if (typeof window !== 'undefined') {
    window.addEventListener('scroll', toggleVisible);
  }

  const scrollToTop = () => {
      window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div>
      <div className='flex justify-center sm:justify-end md:justify-end lg:justify-end w-100 h-20 bg-customSearchColorHovered items-center'>
        <div className="flex items-center">
          <input
            type="text"
            value={request}
            className="w-96 h-12 ml-5 pl-5 pr-16 rounded z-0 focus:shadow focus:outline-none text-gray-900"
            placeholder="Bạn muốn tìm gì..."
            onChange={() => {setRequest(event.target.value)}}
            onKeyDown={(e) => handleSearch(e)}
          />
          <div className='relative right-12 top-0.5'>
            <FontAwesomeIcon
              className='text-gray-900 text-2xl p-2 rounded-full bg-customSearchColor cursor-pointer transition-all ease-in-out duration-400 transform hover:scale-150 active:text-white active:bg-customSearchColorHovered'
              icon={faSearch}
              onClick={(e) => handleSearch(e)}
            />
          </div>    
        </div>
        <Toaster
          position='top-center'
          toastOptions={{
            success: {
              duration: 3000
            },
            error: {
              duration: 3000
            }
          }}
        />
      </div>
      <main className="flex min-h-screen flex-col items-center justify-between lg:p-24 md:p-18 p-10 bg-white text-gray-900">
        <h1 className='lg:text-6xl md:text-5xl text-4xl font-bold mb-24 lg:text-left md:text-left text-center'>
          {title === '' ? 'Bạn đang tìm kiếm điều gì' : title}
        </h1>
        <div className='lg:w-2/3 md:w-3/4 sm:w-4/5 w-full bg-gray-200 border border-solid border-black lg:p-8 md:p-6 p-4'>
          <h2 className='text-3xl font-semibold mb-4 text-center'>
            Nội dung chính của bài viết:
          </h2>
          <ul>
              {infor.map((item, index) => (
                <li key={index} className='p-4 text-blue-600 hover:text-blue-400'>
                  <a href={'#section-' + (index + 1)}>
                    {index + 1}. {item.item}
                  </a>
                </li>
              ))}
            </ul>
        </div>
        <ul>
          {infor.map((item, index) => (
            <li key={index} id={'section-' + (index + 1)} className='ml-2 mr-2 sm:ml-4 sm:mr-4 md:ml-8 md:mr-8 lg:ml-12 lg:mr-12 items-center'>
              <h2 className='text-3xl font-semibold mt-12 mb-12'>
                {index + 1}. {item.item}
              </h2>
              <div className='mb-12'>
                {item.description.split('\n').map((line, index) => (
                  <React.Fragment key={index}>
                    {line}
                    <br />
                  </React.Fragment>
                ))}
              </div>
              {/* <div className='w-full flex justify-center items-center'>
                <img src={item.image} className='w-11/12 sm:w-10/12 md:w-9/12 lg:w-8/12'/>
              </div> */}
            </li>
          ))}
        </ul>
        <FontAwesomeIcon
          className={newArrowClass}
          icon={faArrowUp}
          onClick={() => scrollToTop()}
        />
      </main>
    </div>
  )
}