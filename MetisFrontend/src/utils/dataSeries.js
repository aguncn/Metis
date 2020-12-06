import moment from 'moment'

/**
 * 以下这个函数是为viser写的，感觉这个还不够成熟，换成v-charts。
 * demo sample
[{
  date: '2018/8/1',
  type: 'download',
  value: 4623
}, {
  date: '2018/8/1',
  type: 'register',
  value: 2208
}, {
  date: '2018/8/1',
  type: 'bill',
  value: 182
}]

export function dataSeries (dataTime, dataA, dataB, dataC) {
	let data = []
	const dataAAray = dataA.split(',')
	const dataBAray = dataB.split(',')
	const dataCAray = dataC.split(',')
	for (var i = 0; i < dataAAray.length; i++){
		data.push({
			date: moment(dataTime, 'YYYY-MM-DD HH:mm:ss').subtract(dataAAray.length-i-1,'minutes').format('YY-MM-DD HH:mm:ss'),
			type: 'dataA',
			value: dataAAray[i]
		})
	}
	for (var i = 0; i < dataBAray.length; i++){
		data.push({
			date: moment(dataTime, 'YYYY-MM-DD HH:mm:ss').subtract(Math.floor(dataCAray.length/2)-i,'minutes').format('YY-MM-DD HH:mm:ss'),
			type: 'dataB',
			value: dataBAray[i]
		})
	}
	for (var i = 0; i < dataCAray.length; i++){
		data.push({
			date: moment(dataTime, 'YYYY-MM-DD HH:mm:ss').subtract(Math.floor(dataCAray.length/2)-i,'minutes').format('YY-MM-DD HH:mm:ss'),
			type: 'dataC',
			value: dataCAray[i]
		})
	}
  return data
}
 */

/**
 * v-charts。
 * demo sample
{
	columns: ['日期', '访问用户', '下单用户', '下单率'],
	rows: [
		{ '日期': '1/1', '访问用户': 1393, '下单用户': 1093, '下单率': 0.32 },
		{ '日期': '1/2', '访问用户': 3530, '下单用户': 3230, '下单率': 0.26 },
		{ '日期': '1/3', '访问用户': 2923, '下单用户': 2623, '下单率': 0.76 },
		{ '日期': '1/4', '访问用户': 1723, '下单用户': 1423, '下单率': 0.49 },
		{ '日期': '1/5', '访问用户': 3792, '下单用户': 3492, '下单率': 0.323 },
		{ '日期': '1/6', '访问用户': 4593, '下单用户': 4293, '下单率': 0.78 }
	]
}
 */
export function dataSeries (dataTime, dataA, dataB, dataC) {
	let data = {}
	data.columns =  ['日期', '检测曲线', '昨日曲线', '一周前曲线']
	data.rows = []
	const dataAAray = dataA.split(',')
	const dataBAray = dataB.split(',')
	const dataCAray = dataC.split(',')
	for (var i = 0; i < dataBAray.length; i++){
		data.rows.push({
			'日期': moment(dataTime, 'YYYY-MM-DD HH:mm:ss').subtract(dataAAray.length-i-1,'minutes').format('HH:mm:ss'),
			'检测曲线': dataAAray[i],
			'昨日曲线': dataBAray[i],
			'一周前曲线': dataCAray[i]
		})
	}
  return data
}
