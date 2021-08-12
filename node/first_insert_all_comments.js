const admin = require('firebase-admin');
const serviceAccount = require("./serviceAccountKey.json");
const data = require("./video_comments.json");
//const collectionKey = "youtube-comments"; //name of the collection
//const collectionKey = "comments-reviews"; //name of the collection
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://eletronics-sentiment-analysis-default-rtdb.firebaseio.com"
  //databaseURL: "https://testes-2eb48.firebaseio.com"
});
const firestore = admin.firestore();
const settings = {timestampsInSnapshots: true};
firestore.settings(settings);
if (data && (typeof data === "object")) {
Object.keys(data).forEach(docKey => {
    
    //console.log(data[docKey]['comment-id']);
    //'{"number-of-revised": 0}'
    //data[docKey]
    //nbm_revised = JSON.parse('{"number-of-revised": 0}');
    //console.log(data)
    
    firestore.collection("youtube-comments").doc(docKey).set(data[docKey]).then((res) => {
        console.log("Document " + docKey + " successfully written!");
    }).catch((error) => {
        console.error("Error writing document: ", error);
    });


});
}