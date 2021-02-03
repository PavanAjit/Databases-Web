import React from 'react'
import axios from 'axios'
import QBEInterface from './QBEInterface';

function DataBaseTables(props) {
  // const range=[{key:0,text:0,value:0},{key:1,text:1,value:1},{key:2,text:2,value:2}];
  const tableDict={}
  const skeleton={}
  let[tableCount,setTableCount]=React.useState('')
  let[skeletonData,setSkeletonData]=React.useState('')

  const getSkeletons = e => {
    e.preventDefault()
    for (var key in props.tables){
      tableDict[props.tables[key]]='';
    }
    
    for(var key in tableDict){
      var e=document.getElementById(key);
      tableDict[key]=e.value;
    }
    setTableCount(tableDict)
    const queryString='columns(user:"'+props.username+'",passwd:"'+props.password+'",database:"'+props.database+'"){column,table}'
    const url="http://127.0.0.1:5000/graphql?query={"+queryString+"}"
    axios.get(url)
    .then((response)=>{
      var skel;
      for (skel of response.data.data.columns){
        if (!skeleton[skel.table]) {
        skeleton[skel.table] = [skel.column];
        }
        else{
          skeleton[skel.table].push(skel.column);        
        }
      }
      // alert(JSON.stringify(tableCount))
      setSkeletonData(skeleton)
      // alert(JSON.stringify(skeleton))
    })
    .catch((error) => {
      alert(error)
    })
      
    };

  const resetSkeletons = e => {
      setSkeletonData('')
    };

  const checkSelected=e=>{
    // tableDict.push({key:e.target.id,value:e.target.value})
    tableDict[e.target.id]=e.target.value
    // alert(JSON.stringify(tableDict))
  }

    return (
      <div className="DataBaseTables">
        <header className="DataBaseTables-header" style={{marginTop:'25px',marginLeft:'25px'}}>
            <label id='DataBaseTableslbl' style={{color:'#003399'}}><b>Database Tables</b></label>
            <br/>
            {/* <ul>
                            {props.tables.map(table =>
                              <li tableLbl={table.tablename}>{table.tablename}</li>
                            )}
                        </ul>  */}
            <table>
                <thead>
                    <tr style={{textAlign:'left'}}>
                    <th>Database</th>
                    <th>Count</th>
                    </tr>
                </thead>
                <tbody>
                  {/* <td>
                    {props.tables.map(table =><tr>{table.tablename}</tr>)}
                    <tr><button onClick={getSkeletons}>Get Skeletons</button></tr>
                  </td>
                  <td>
                    {props.tables.map(table =>
                      <tr>
                        <select id={table.tablename} onChange={checkSelected}>
                            <option value="0" selected>0</option>
                            <option value="1" >1</option>
                            <option value="2">2</option>
                        </select>
                      </tr>)}
                      <tr><button onClick={resetSkeletons}>Reset Skeletons</button></tr>
                  </td> */}
                  <td>
                    {props.tables.map(table =><tr style={{height:'25px'}}>{table}</tr>)}
                    <tr style={{height:'25px'}}><button onClick={getSkeletons}>Get Skeletons</button></tr>
                  </td>
                  <td>
                    {props.tables.map(table =>
                      <tr style={{height:'25px'}}>
                        <select id={table} >
                            <option value="0" selected>0</option>
                            <option value="1" >1</option>
                            <option value="2">2</option>
                        </select>
                      </tr>)}
                      <tr style={{height:'25px'}}><button onClick={resetSkeletons}>Reset Skeletons</button></tr>
                  </td>
                </tbody>
            </table>
        </header>
        {(skeletonData && <QBEInterface tableSkeleton={skeletonData} username={props.username} password={props.password} database={props.database} tblCount={tableCount}/>) || ""}
      </div>
    );
  }

  export default DataBaseTables;