import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class ProcesadorEDA:
    def __init__(self, df):
        self.df = df

    def tendencia_anual(self):
        plt.figure()
        trend = self.df.groupby('Año').size()
        sns.lineplot(x=trend.index, y=trend.values, marker='o', color='teal')
        plt.title('Evolución Anual de Accidentes')
        plt.xlabel('Año')
        plt.ylabel('Cantidad')
        plt.show()

    def top_provincias(self):
        plt.figure()
        order = self.df['Provincia'].value_counts().index
        sns.countplot(data=self.df, y='Provincia', order=order, palette='viridis')
        plt.title('Accidentes por Provincia')
        plt.xlabel('Cantidad')
        plt.show()

    def tipo_accidentes_top10(self):
        plt.figure()
        top10 = self.df['Tipo de accidente'].value_counts().head(10)
        sns.barplot(x=top10.values, y=top10.index, palette='magma')
        plt.title('Top 10 Tipos de Accidentes')
        plt.xlabel('Número de Casos')
        plt.show()

    def distribucion_semana(self):
        plt.figure()
        orden = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        sns.countplot(data=self.df, x='Día', order=orden, palette='coolwarm')
        plt.title('Accidentes por Día de Semana')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)
        plt.show()