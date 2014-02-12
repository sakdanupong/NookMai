function summaryNumber(i_num) {
	var result = '';
	var len = i_num.toString().length;
	if (len < 4) 
		return i_num + ''

	var dePlace = 0;
	var fraction = i_num % 1000;
	var dec = fraction % 100;

	if (fraction != 0) {
		if (dec == 0)
			dePlace = 1;
		else
			dePlace = 2;	
	}
	
	result = (i_num / 1000).toFixed(dePlace) + 'k';
	return result;
}