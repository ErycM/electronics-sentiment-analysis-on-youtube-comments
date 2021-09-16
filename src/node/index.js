const admin = require('./node_modules/firebase-admin');
const serviceAccount = require("./serviceAccountKey_teste.json");
//const data = require("./video_comments.json");
//const collectionKey = "youtube-comments"; //name of the collection
//const collectionKey = "comments-reviews"; //name of the collection
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  //databaseURL: "https://eletronics-sentiment-analysis-default-rtdb.firebaseio.com"
  databaseURL: "https://testes-2eb48.firebaseio.com"
});
const firestore = admin.firestore();
const settings = {timestampsInSnapshots: true};
firestore.settings(settings);
    

// const youtubeComments = db.collection('youtube-comments');
// const snapshot = await youtubeComments.get();
// snapshot.forEach(doc => {
// console.log(doc.id, '=>', doc.data());
// });

function arrayToCSV(objArray) {
    const array = typeof objArray !== 'object' ? JSON.parse(objArray) : objArray;
    let str = `${Object.keys(array[0]).map(value => `"${value}"`).join(",")}` + '\r\n';

    return array.reduce((str, next) => {
        str += `${Object.values(next).map(value => `"${value}"`).join(",")}` + '\r\n';
        return str;
       }, str);
}

//const fs = require('fs');
console.log("entrou");
firestore.collection("video-comments-reviews").doc('1.Ugy7sSdqZBNru0HSeb94AaABAg').then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
        // doc.data() is never undefined for query doc snapshots
        
        //console.log(doc.id, " => ", doc.data());
        
        console.log(doc.id+","+arrayToCSV([doc.data()]));

        //fs.appendFile('video_comments_reviews.csv', doc.id+","+arrayToCSV([doc.data()]), function (err) {
        //    if (err) throw err;
        //    console.log(doc.id+' Saved!');
        //});


    });
}).catch((error) => {
    console.error("Error get document: ", error);
});


