export const apiUrl = 'https://wxapi.rp-i.net/'

export const formatDateTime = (dateTimeStr) => {
  // 创建日期对象
  const date = new Date(dateTimeStr)
  // 获取年、月、日、小时、分钟和秒
  const year = date.getFullYear()
  const month = date.getMonth() + 1 // 月份从0开始，需要加1
  const day = date.getDate()
  const hours = date.getHours()
  const minutes = date.getMinutes()
  const seconds = date.getSeconds()
  // 格式化为指定的字符串格式
  return `${year}年${_formatDateTimeZero(month)}月${_formatDateTimeZero(day)}日 ${_formatDateTimeZero(hours)}:${_formatDateTimeZero(minutes)}:${_formatDateTimeZero(seconds)}`
}
// 辅助函数：确保时间格式中分钟和秒为两位数
const _formatDateTimeZero = (num) => {
  return num < 10 ? '0' + num : num
}

export const formatTime = (date: Date) => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return (
    [year, month, day].map(formatNumber).join('/') +
    ' ' +
    [hour, minute, second].map(formatNumber).join(':')
  )
}

const formatNumber = (n: number) => {
  const s = n.toString()
  return s[1] ? s : '0' + s
}
