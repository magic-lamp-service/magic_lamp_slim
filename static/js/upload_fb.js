function upload_img(file, id){
    const firebaseConfig = {
        apiKey: "AIzaSyAhmK8KCg_zVRHr3TJRI6FvfC4rYx0EAk4",
        authDomain: "magic-lamp-68a36.firebaseapp.com",
        projectId: "magic-lamp-68a36",
        storageBucket: "magic-lamp-68a36.appspot.com",
        messagingSenderId: "113869546380",
        appId: "1:113869546380:web:29149576edb7e7f90b2ca9"
    };

    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);

    // Get a reference to the storage service, which is used to create references in your storage bucket
    var storage = firebase.storage();

    var storageRef = storage.ref(id + '.png');
    var task = storageRef.put(file);
    // monitor the upload progress
    task.on('state_changed',
    function progress(snapshot) {
        var percent = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        console.log(percent + '% uploaded');
    },
    function error(err) {
        console.log('Upload failed: ' + err.message);
    },
    function complete() {
        console.log('Upload complete');
        }
    );
    return new Promise(function(resolve, reject) {
        task.on('state_changed', null, reject, function() {
            // get the download URL of the uploaded image
            storageRef.getDownloadURL().then(resolve);
        });
    });
}