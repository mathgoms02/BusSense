export const arrayToSql = (array: string[]) : string =>
     !array.length ? null : "('" + array.join("','") + "')";
  
export const setPlaceholders = (array: string[]) => {
  const offset = 1;
  return '(' + array.map(function(name,i) { 
      return '$'+(i+offset); 
  }).join(',') + ')';
}
