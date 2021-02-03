var tableList;                      // Array of all the tables in Database
var tableDropdownList = [];         // List of autogenerated dropdown names for tables
var columnList;                     // List of columns from the Python Server
var qbeInputFieldsList = [];        // List of Ids whose data to send to server for qbe2sql

// This function calls the server, and checks for credentials
async function loadTables() {
    const response = await fetch('http://localhost:5000/graphql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
            {
                query: `query { tables (user:"${txtUser.value}", 
              passwd:"${txtPasswd.value}", 
              database:"${txtDb.value}") }`
            }
        ),
    }).then(response => response.json());

    if (response["errors"] !== undefined) {
        // If errors found in Graphql response, something is wrong
        alert("The Credentials entered are incorrect. Please enter valid credentials!");
    } else {
        // No errors found in Graphql response. so we create the list of tables
        tableList = response.data.tables;
        await generateSkeleton();
    }
}

async function generateSkeleton() {
    placeholderDivElement = document.getElementById("dbTablesContainer");
    tableDropdownList = [];
    // Run through all tables
    
    dbTableHTMLSting = `
    <hr><div class="row">
    <div class="col-sm">
    <h3 class="display-10">Database Tables</h3>
    </div></div><div class="row">`;

    for (table of tableList) {
        dbTableHTMLSting +=
            `<div class="col-sm">${table}:  
        <select class="form-select" id="tableDropdown${table}">
        <option selected value="0">0</option>
        <option value="1">1</option>
        <option value="2">2</option>
        </select></div>
        `;
        tableDropdownList.push(`${table}`);
    }
    dbTableHTMLSting += 
    `</div><br><div class="row">
    <div class="col-sm">
        <button type="button" class="btn btn-primary" onclick="getSkeleton()">Get Skeleton</button> 
        <button type="button" class="btn btn-primary" onclick="resetSkeleton()">Reset Skeleton</button> 
    </div>
    `;

    placeholderDivElement.innerHTML = dbTableHTMLSting;
    console.log(tableDropdownList);
}

async function getSkeleton() {
    // Create skeleton for all the dropdowns that has a non zero value
    placeholderDivElement = document.getElementById("qbeInterfaceContainer");
    var qbeInterfaceHTMLString = `<div class="row">
    <div class="col-sm">
    <h3 class="display-10">QBE Interface</h3>
    </div></div>`;
    placeholderDivElement.innerHTML = "<hr>";
    qbeInputFieldsList = [];
    const response = await fetch('http://localhost:5000/graphql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
            {
                query: `query { columns (user:"${txtUser.value}", 
              passwd:"${txtPasswd.value}", 
              database:"${txtDb.value}") { 
                column
                datatype
                table} }`
            }
        ),
    }).then(response => response.json());

    if (response["errors"] !== undefined) {
        // If errors found in Graphql response, something is wrong
        alert("Unable to generate Skelton. Please check your credentials!");
    } else {
        // No errors found in Graphql response. so we create the list of tables
        columnList = response.data.columns;
        console.log(columnList);

        // for every dropdown
        for(table of tableList) {
            tempDropDown = document.getElementById(`tableDropdown${table}`);
            if (tempDropDown.value > 0) {
                for (i=1; i<=tempDropDown.value ; i++) {
                    qbeInterfaceHTMLString += `
                    <table class="table">
                    <tr class="table-primary">
                    <td>${table}</td>`;
                    for(column of columnList) {
                        if (column.table === table) {
                            qbeInterfaceHTMLString += `<td>${column.column}
                            (${column.datatype})</td>`
                        }
                    }
                    
                    tableTextId = `${table}_${i-1}`;
                    qbeInputFieldsList.push(tableTextId);
                    
                    qbeInterfaceHTMLString += `
                    </tr>
                    <tr class="table">
                    <td><input type="text" style="text-transform: uppercase" id="${tableTextId}"></td>`;
                    for(column of columnList) {
                        if (column.table === table) {
                            columnTextId = `${tableTextId}.${column.column}`;
                            qbeInputFieldsList.push(columnTextId);
                            qbeInterfaceHTMLString += `<td><input type="text" style="text-transform: uppercase" id="${columnTextId}"></td>`
                        }
                    }
                    qbeInterfaceHTMLString += `
                    </tr>
                    </table></br>
                    `
                }
            }
        }
        console.log(qbeInputFieldsList);


        qbeInterfaceHTMLString += `
        <div class="row">
        <div class="col-sm">
            Condition: <input type="text" style="text-transform: uppercase" id="txtCondition">
        </div>
        </div>
        <br/>
        <div class="row">
        <div class="col-sm">
            <button type="button" class="btn btn-primary" onclick="query()">Run Query</button> 
        </div>
        </div>
        `;
        console.log(qbeInputFieldsList);

        placeholderDivElement.innerHTML += qbeInterfaceHTMLString;

    }
}

async function resetSkeleton() {
    document.getElementById("qbeInterfaceContainer").innerHTML = "";
    document.getElementById("queryResultsContainer").innerHTML = "";
    for (table in tableList) {
        tempItem = document.getElementById(`tableDropdown${tableList[table]}`);
        tempItem.value = 0;
    }
    
}

async function query() {
    // This function reads all the inputs and creates a server query
    var jsonQuery = [];
    var placeholderDivElement = document.getElementById("queryResultsContainer");
    var queryTableHTML = "";

    // {"field": field, "value": value}
    for (field of qbeInputFieldsList) {
        jsonQuery.push(
            {
                "field": field, 
                "value": document.getElementById(field).value
            });
    }
    jsonQuery.push({"field": "Condition", 
    "value": document.getElementById("txtCondition").value})
    console.log(jsonQuery);

    jsonQuery = btoa(JSON.stringify(jsonQuery));

    // Now we call the server

    const response = await fetch('http://localhost:5000/graphql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
            {
                query: `query { qbe (user:"${txtUser.value}", 
              passwd:"${txtPasswd.value}", 
              database:"${txtDb.value}",
              qbequery:"${jsonQuery}") }`
            }
        ),
    }).then(response => response.json());

    if (response["errors"] !== undefined) {
        // If errors found in Graphql response, something is wrong
        alert(`${response.errors[0].message}`);
    } else {
        // No errors found in Graphql response. so we create the list of tables
        var querytoDisplay =response.data.qbe[0];
        var tableDatatoDisplay = JSON.parse(response.data.qbe[1]);
        
        queryTableHTML += `<hr>
        <div class="row">
        <div class="col-sm">
        <h3 class="display-10">Query Results</h3>
        </div></div>
        <div class="row">
        <div class="col-sm">
            <b>SQL Query: </b><br>${querytoDisplay}
        </div>
        </div>
        <br/>
        <table class="table">`

        row_count = 0;
        for(row of tableDatatoDisplay) {
            if (row_count == 0) {
                // For header row
                queryTableHTML += `<tr class="table-primary">`
            } else {
                queryTableHTML += `<tr>`
            }
            
            for (col of row) {
                queryTableHTML += `<td>${col}</td>`
            }
            queryTableHTML += `</tr>`
            row_count +=1 ;
        }
        
        queryTableHTML += `</table>`
        
        placeholderDivElement.innerHTML = queryTableHTML;
    }
}