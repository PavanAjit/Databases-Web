import React from 'react'
import axios from 'axios'
import DataBaseTables from './DataBaseTables';



function Login() {
    let [responseData, setResponseData]= React.useState('')
    let [username,setUserName]= React.useState('')
    let[password,setPassword]= React.useState('')
    let[database,setDatabase] = React.useState('')
    // const dat={data:{data:{tables:{}}}}
    // setResponseData(dat)
    // const handleLogin=()=> {
    
    // fetches data
    const fetchData = (e) => {
        e.preventDefault()
        // axios.get('/classrooms/?query={tables{tablename}}')
        // const queryString='tables(username:"'+username+'",password:"'+password+'",database:"'+database+'"){tablename}'
        const queryString='tables(user:"'+username+'",passwd:"'+password+'",database:"'+database+'")'
        const url="http://127.0.0.1:5000/graphql?query={"+queryString+"}"
        // alert(queryString)
        // alert(url)
        axios.get(url)
        // fetch("/classrooms/?query={tables(username:"+username+",password:"+password+",database:"+database+"){tablename}}", {
        //         method: "GET",
        //         headers: {
        //         "Content-Type": "application/json",
        //         }
        //         // body: JSON.stringify({
        //         // query: "query{tables(username:"+username+",password:"+password+",database:"+database+"){tablename}}",
        //         // }),
        //     })
        .then((response)=>{
            setResponseData(response.data)
            // alert(JSON.stringify(responseData.data.tables))
        })
        .catch((error) => {
            alert(error)
        })
      }
//   }

  const handleUsernameChange = e => {
    setUserName(e.target.value)
  };

  const handlePasswordChange = e => {
    setPassword(e.target.value)
  };

  const handleDatabaseChange = e => {
    setDatabase(e.target.value)
  };
  

    return (
        <div className="Login">
          <header className="Login-header" style={{marginTop:'25px',marginLeft:'25px'}}>
              <label id='QBElbl' style={{color:'#003399'}}><b>QBE</b></label>
              <br/>
              <table>
                  <thead>
                      <tr>
                      <th></th>
                      <th>User Name</th>
                      <th>Password Name</th>
                      <th>Database</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr>
                      <td>MySQL</td>
                      <td><input type="text" id="userName" onChange={handleUsernameChange}></input></td>
                      <td><input type="password" id="password" onChange={handlePasswordChange}></input></td>
                      <td><input type="text" id="database" onChange={handleDatabaseChange}></input></td>
                      <td><button onClick={fetchData}>Go</button></td>
                      </tr>
                  </tbody>
              </table>
          </header>
          {(responseData && <DataBaseTables tables={responseData.data.tables} username={username} password={password} database={database}/>) || ""}
          {/* <DataBaseTables tables={responseData.data.tables}/> */}
        </div>
    )
}

export default Login
