CaminhoArquivoExcel = "C:\Users\supor\OneDrive\PowerBi\Relatorios\Dados Resumidos\NFE_U.xlsm"
Set ExcelApp = CreateObject("Excel.Application") 
ExcelApp.Visible = True
ExcelApp.DisplayAlerts = False 
Set wb = ExcelApp.Workbooks.Open(CaminhoArquivoExcel) 
wb.RefreshAll 
wb.Save 
wb.Close 
ExcelApp.DisplayAlerts = True
ExcelApp.Quit 
   
   
