console.log('Loading function');

exports.handler = async (event, context) => {
    /* Process the list of records and transform them */
    const output = event.records.map((record) => {
        console.log("record : " + JSON.stringify(record))
        let newDataString = atob(record.data);
        console.log("data : " + newDataString);
        let newData = JSON.parse(newDataString);

        console.log("service : " + newData.service);
        if (newData.service == 'kim.jeonghyeon.slackbotaya') {
            let reg = /user:(.+?), where:(.*?), action:(.+?), detail:(.*)/g;
            let regResult = reg.exec(newData.message)
            if (regResult != null) {
                newData.user = regResult[1]
                newData.where = regResult[2]
                newData.action = regResult[3]
                newData.detail = regResult[4]
            }
        }
        console.log("success")
        return {
            /* This transformation is the "identity" transformation, the data is left intact */
            recordId: record.recordId,
            result: 'Ok',
            data: btoa(JSON.stringify(newData)),
        };
    });
    console.log(`Processing completed.  Successful records ${output.length}.`);
    return { records: output };
};


//Base64 decoding
function atob(data) {
    try {

        let buff = Buffer.from(data, 'base64');//new Buffer(data, 'base64');
        return buff.toString('utf-8');
    } catch(e) {
        //sometimes receive data without base64 encoding
        return data
    }

}

//Base64 encoding
function btoa(data) {
    let buff = Buffer.from(data);
    return buff.toString('base64');
}