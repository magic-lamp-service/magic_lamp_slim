const csrf = document.getElementsByName('csrfmiddlewaretoken')
const imageForm = document.getElementById('image-form')
const imageBox = document.getElementById('image-box')
const confirmBtn = document.getElementById('confirm-btn')
const input = document.getElementById('id_file')
const image_setting_container = document.getElementById('image_setting_container')
const image_text =document.getElementById('image_text')
const clock_dot = document.getElementById('clock_dot')
const crop_container_height = 300

var zoom_flag, original_height, zoom_height, zoom;
var text_to_image_ratio;
let crop_image = null;
var cropper_width = null;

$("#image_text").removeClass("hidden")
$("#confirm_container").removeClass("hidden")
$("#image-form").removeClass('float-center')
    
var isInitialized = false

var image_ratio_x = $('#confirm-btn').attr('data-image_ratio_x')
var image_ratio_y = $('#confirm-btn').attr('data-image_ratio_y')

image_setting_container.classList.remove('hidden')
zoom = 1
zoom_flag = true
text_to_image_ratio = 0.1
console.log('img url:', url)
imageBox.innerHTML = `<img src="${url}" id="image" width="700px">`

const image = document.getElementById('image');
crop_image = new Cropper(image, {
    aspectRatio: image_ratio_x / image_ratio_y,
    viewMode: 1,
    dragMode: false,
    checkOrientation: false,
    cropBoxMovable: false,
    cropBoxResizable: false,
    zoomOnTouch: false,
    zoomOnWheel: false,
    guides: false,
    highlight: false,
    autoCropArea: 1,

    ready: function (e) {
        var cropper = this.cropper;
        cropper.zoomTo(0);

        var imageData = cropper.getImageData();
        console.log("imageData ", imageData);
        $('#image_text').css({
            'font-size': imageData.height * text_to_image_ratio
        })

        var crop_box = $('.cropper-crop-box')
        var crop_box_offsets = crop_box.offset()
        console.log(crop_box_offsets)
        x_pos = crop_box_offsets.top
        y_pos = crop_box_offsets.left

        const cropper_crop_box = document.getElementsByClassName('cropper-crop-box')[0]
        if(cropper_width == null){
            cropper_width = cropper_crop_box.offsetWidth
        }

        cropper_crop_box.appendChild(image_text)
        cropper_crop_box.appendChild(clock_dot)

        
        $('#color').colorpicker().val('#ffffff')
        $('#color').colorpicker().on('changeColor',
            function (ev) {
                $('#image_text').css('color', $(this).val())
        });
        
        $('#image_text_input').on('change keydown paste input', function (e) {
            if($('#image_text').width() < cropper_width - cropper_width*0.05 || e.key === "Backspace" || e.key === "Delete"){
                $('#image_text').text($(this).val())
            }
            else{
                e.preventDefault();
                console.log("dont add more text" + $('#image_text').width() + " " + cropper_width)
            }
        });
        
        $('#text_font').on('change', function(e){
            if(image_text.offsetWidth < cropper_width - cropper_width*0.05){
                    $('#image_text').css({
                    'font-family': this.value
                })
            }
            else{
                $('#image_text').css({
                    'font-family': "Abraham"
                })
            }                
        })

        $('#slider_input').on('input change', () => {
            slider_val = $('#slider_input').val()
            $('#start_slider_value').html(slider_val);
            if (isInitialized == true) {
                if (crop_image.canvasData.naturalWidth < 600 || crop_image.canvasData.naturalHeight < 400) {
                    event.preventDefault();
                } else {
                    var zoomValue = parseFloat(slider_val / 100).toFixed(4)
                    console.log(zoomValue)
                    crop_image.zoomTo(zoomValue)
                }
            }
        });
    },

    crop(event) {
        console.log('x: ' + event.detail.x);
        console.log('y: ' + event.detail.y);
        console.log('width: ' + event.detail.width);
        console.log('height: ' + event.detail.height);
        console.log('rotate: ' + event.detail.rotate);
        console.log('scaleX: ' + event.detail.scaleX);
        console.log('scaleY: ' + event.detail.scaleY);
        console.log('slider input' + $("#slider_input").val());
        if (zoom_flag == true){
            zoom_flag = false
            original_height = event.detail.height
        }
        zoom_height = event.detail.height
        zoom = original_height / zoom_height
        console.log('zoom: ' + zoom)
    },
});

isInitialized = true;

$('#confirm-btn').click(function () {

    var img = new Image()
    img.src = url
    console.log('productId:', productId, 'Action:', action)                

    //var imageId = (new Date()).getTime()
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('image_id:', imageId)
    console.log('productId:', productId, 'Action:', action)
    console.log('USER:', user)
    
    img.onload = function() {
        $("#loading").removeClass("hidden")

        var canvas = crop_image.getCroppedCanvas()
        var context = canvas.getContext('2d');

        var text = $('#image_text_input').val()

        //var zoom_in = (1 - $("#slider_input").val())* 0.01
        var realTextSize = img.height * text_to_image_ratio
        
        context.fillStyle = 'white'

        context.strokeStyle = "gray";
        context.lineWidth = realTextSize / 25;
        
        context.font = realTextSize + 'px ' + $('#image_text').css("font-family")
        var textWidth = context.measureText(text).width;
    
        console.log("text_spacer_from_top:" + text_spacer_from_top)
        context.fillText($('#image_text_input').val() ,canvas.width/2 - textWidth/2 ,canvas.height*text_spacer_from_top);
        context.strokeText($('#image_text_input').val() ,canvas.width/2 - textWidth/2 ,canvas.height*text_spacer_from_top);

        canvas.toBlob((blob) => {
            console.log('confirmed')
            const fd = new FormData()
            upload_img(blob, imageId)
            .then(function(fb_url) {
                // do something with the URL of the uploaded image
                console.log('fb url', fb_url);

                fd.append('csrfmiddlewaretoken', csrf[0].value)
                fd.append('fb_link', fb_url)
                fd.append('image_id', imageId)
                var is_text = true
                if($('#image_text_input').val() == "" || $('#image_text_input').val() == null){
                    is_text = false
                }
                if (is_text){
                    fd.append('is_text', true)
                    fd.append('text', $('#image_text_input').val())
                    fd.append('text_font', $('#image_text').css("font-family"))
                }
                console.log(Array.from(fd))
                // send the POST request using fetch
                fetch('/moon_lamp_editor/' + imageId, {
                    method: 'POST',
                    body: fd
                })
                .then(response => {
                    if (response.ok) {
                        // handle the successful response
                        console.log('Request succeeded:', response);
                        if (user == 'AnonymousUser') {
                            addCookieItem(productId, action, imageId)
                        } else {
                            updateUserOrder(productId, action, imageId)
                        }    

                    } else {
                        // handle the unsuccessful response
                        console.error('Request failed:', response.status);
                    }
                })
                .catch(error => {
                    // handle any errors
                    console.error(error);
                });    
            })
            .catch(function(error) {
                // handle any errors
                console.error(error);
            });
        })
    }
    
})    
