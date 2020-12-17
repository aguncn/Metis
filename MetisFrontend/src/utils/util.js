import enquireJs from 'enquire.js'

export function isDef (v){
  return v !== undefined && v !== null
}

/**
 * Remove an item from an array.
 */
export function remove (arr, item) {
  if (arr.length) {
    const index = arr.indexOf(item)
    if (index > -1) {
      return arr.splice(index, 1)
    }
  }
}

export function isRegExp (v) {
  return _toString.call(v) === '[object RegExp]'
}

export function enquireScreen(call) {
  const handler = {
    match: function () {
      call && call(true)
    },
    unmatch: function () {
      call && call(false)
    }
  }
  enquireJs.register('only screen and (max-width: 767.99px)', handler)
}

const _toString = Object.prototype.toString

export function randomString(randomLen, min, max){
    var str = "",
        range = min,
        arr = ['2', '3', '4', '5', '7', '8', 
               'a', 'c', 'd', 'e', 'f', 'h', 'j', 'k',
               'm', 'n', 'p', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'H', 'J', 'K', 'L', 'M', 'N', 'P', 
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    // 随机产生
    if(randomLen){
        range = Math.round(Math.random() * (max-min)) + min;
    }
    for(var i=0; i<range; i++){
        let pos = Math.round(Math.random() * (arr.length-1));
        str += arr[pos];
    }
    return str;
}

/**
 * 判断变量是否为空，
 * @param  {[type]}  param 变量
 * @return {Boolean}      为空返回true，否则返回false。
 */
export function isEmpty(param){
    if(param){
        var param_type = typeof(param);
        if(param_type == 'object'){
            //要判断的是【对象】或【数组】或【null】等
            if(typeof(param.length) == 'undefined'){
                if(JSON.stringify(param) == "{}"){
                    return true;//空值，空对象
                }
            }else if(param.length == 0){
                return true;//空值，空数组
            }
        }else if(param_type == 'string'){
            //如果要过滤空格等字符
            var new_param = param.trim();
            if(new_param.length == 0){
                //空值，例如:带有空格的字符串" "。
                return true;
            }
        }else if(param_type == 'boolean'){
            if(!param){
                return true;
            }
        }else if(param_type== 'number'){
            if(!param){
                return true;
            }
        }
        return false;//非空值
    }else{
        //空值,例如：
        //(1)null
        //(2)可能使用了js的内置的名称，例如：var name=[],这个打印类型是字符串类型。
        //(3)空字符串''、""。
        //(4)数字0、00等，如果可以只输入0，则需要另外判断。
        return true;
    }
}