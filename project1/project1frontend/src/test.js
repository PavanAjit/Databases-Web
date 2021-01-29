import React from 'react'
import axios from 'axios'
import DataBaseTables from './DataBaseTables';



function Test() {
    let [responseData, setResponseData] = React.useState('')
    // const handleLogin=()=> {
    
    // fetches data
    const fetchData = (e) => {
        e.preventDefault()
        axios.get('/classrooms/?query={tables{tablename}}')
        .then((response)=>{
            setResponseData(response.data)
            alert(JSON.stringify(responseData.data.tables))
        })
        .catch((error) => {
            alert(error)
        })
      }
//   }

//   const handleUsernameChange = e => {
//     this.setState({
//       username: e.target.value
//     });
//   };

//   const handlePasswordChange = e => {
//     this.setState({
//       password: e.target.value
//     });
//   };

//   const handleDatabaseChange = e => {
//     this.setState({
//       database: e.target.value
//     });
//   };
  

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
                      <td><input type="text" id="userName"  ></input></td>
                      <td><input type="password" id="password"  ></input></td>
                      <td><input type="text" id="database" ></input></td>
                      <td><button onClick={fetchData}>Go</button></td>
                      </tr>
                  </tbody>
              </table>
          </header>
          <DataBaseTables tables={responseData.data.tables}/>
        </div>
    )
}

export default Test
