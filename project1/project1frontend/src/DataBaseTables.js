

function DataBaseTables(props) {
  const range=[{key:0,text:0,value:0},{key:1,text:1,value:1},{key:2,text:2,value:2}];
  const tableDict={}

  const getSkeletons = e => {
      
    };

  const resetSkeletons = e => {
      
    };

  const checkSelected=e=>{
    // tableDict.push({key:e.target.id,value:e.target.value})
    tableDict[e.target.id]=e.target.value
    alert(JSON.stringify(tableDict))
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
                    <tr>
                    <th>Database</th>
                    
                    </tr>
                </thead>
                <tbody>
                  <td>
                    {/* {props.tables.map(table =><tr tableLbl={table.tablename}>{table.tablename}</tr>)} */}
                    {props.tables.map(table =><tr>{table.tablename}</tr>)}
                    <tr><button onClick={getSkeletons}>Get Skeletons</button></tr>
                  </td>
                  <td>
                    {props.tables.map(table =>
                      // <tr tableSelect={table.tablename}>
                      <tr>
                        <select id={table.tablename} onChange={checkSelected}>
                            <option value="0" selected>0</option>
                            <option value="1" >1</option>
                            <option value="2">2</option>
                        </select>
                      </tr>)}
                      <tr><button onClick={resetSkeletons}>Reset Skeletons</button></tr>
                  </td>
                </tbody>
            </table>
        </header>
      </div>
    );
  }

  export default DataBaseTables;