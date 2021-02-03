import React from 'react'
import axios from 'axios'



function QBEInterface(props) {
  // alert(JSON.stringify(props.tblCount))
  let[tableCont,setTableCont]=React.useState('');
  let[queryData,setQueryData]=React.useState('')

  const changeText = e => {
    // var tempList=[]
    // tempList.push(e.target.id)
    // for (var x in tableCont){
    //   if(!tempList.includes(tableCont[x])){
    //     tempList.push(tableCont[x])
    //   }
    // }
    // setTableCont(tempList)
    // // alert(JSON.stringify(tableCont))
    };

  const repeatTable=e=>{
    // alert("Inside")
    let tableContent=[]
    for(let item in e)
    {
      for(let i=1;i<=e[item];i++){
        // alert(props.tableSkeleton[item])
        tableContent.push(
          <div>
            <table style={{border:'1px solid black'}}>
              <thead>
                <tr>
                  <th style={{width:'1px',border:'1px solid black'}}>{item}</th>
                  {props.tableSkeleton[item].map(column=><th style={{width:'1px',border:'1px solid black'}}>{column}</th>)}
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <input type="text" id={item+"_"+(i-1)} onChange={changeText}></input>
                  </td>
                  {props.tableSkeleton[item].map(column=><td><input type="text" id={item+"_"+(i-1)+"."+column} onChange={changeText}></input></td>)}
                </tr>
                </tbody>
            </table>
            <br/>
          </div>
          
        )
      }
    }
    return tableContent;    
  }
  const getQuery=e=>{
    var jsonQuery = [];

    for(let item in props.tblCount){
      for(let i=1;i<=props.tblCount[item];i++){
        // alert(item)
        for(let column in props.tableSkeleton[item]){
          // alert((props.tableSkeleton[item])[column])
          jsonQuery.push({
            "field":(item+"_"+(i-1)+"."+(props.tableSkeleton[item])[column]),
            "value":document.getElementById(item+"_"+(i-1)+"."+(props.tableSkeleton[item])[column]).value
          })
        }
        jsonQuery.push({
            "field":(item+"_"+(i-1)),
            "value":document.getElementById(item+"_"+(i-1)).value
          })
      }
    }
    // for(var i in tableCont)
    // {
    //   jsonQuery.push(
    //         {
    //           "field": tableCont[i], 
    //           "value": document.getElementById(tableCont[i]).value
    //         });
    // }
    jsonQuery.push({"field": "Condition","value": document.getElementById("txtCondition").value})
    console.log(JSON.stringify(jsonQuery))
    jsonQuery = btoa(JSON.stringify(jsonQuery));
    
    const queryString='qbe(user:"'+props.username+'",passwd:"'+props.password+'",database:"'+props.database+'",qbequery:"'+jsonQuery+'")'
        const url="http://127.0.0.1:5000/graphql?query={"+queryString+"}"
        axios.post(url)
        .then((response)=>{
            setQueryData(response.data)
            alert(JSON.stringify(queryData))
        })
        .catch((error) => {
            alert(error)
        })
  };

      return (
       <div className="QBEInterface" style={{marginTop:'25px',marginLeft:'25px'}}>
        <header className="QBEInterface-header" style={{marginTop:'25px'}}>
          <div>
            <label id='QBEInterfacelbl' style={{color:'#003399'}}><b>QBE Interface</b></label>
            <br/>
            <br/>
          </div>
          {repeatTable(props.tblCount)}
          Condition: <input type="text" style={{textTransform:'uppercase'}} id="txtCondition"></input>
          <br/>
          <br/>
          <button onClick={getQuery}>Run Query</button>
        </header>
      </div>
    )
}

export default QBEInterface
