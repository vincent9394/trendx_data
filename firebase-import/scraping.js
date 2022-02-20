const mockData = require('./mock_stock_data.json');
const jsonfile = require('jsonfile')


const dataFiltering = () =>{

jsonfile.readFile('./mock_stock_data.json', function (err, obj) {
    if (err) console.error(err)
    console.dir(obj)
  })

}

dataFiltering()