import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizador:
    def __init__(self, df):
        self.df = df

    def mapa_calor_provincia_hora(self):
        plt.figure(figsize=(14, 8))
        ct = pd.crosstab(self.df['Provincia'], self.df['Hora recodificada'])
        sns.heatmap(ct, annot=True, fmt="d", cmap="YlGnBu")
        plt.title('Provincia vs Rango Horario')
        plt.ylabel('Provincia')
        plt.xlabel('Rango Horario')
        plt.show()

    def mapa_calor_canton_zona(self):
        plt.figure(figsize=(12, 10))
        top = self.df['Cantón'].value_counts().nlargest(20).index
        df_sub = self.df[self.df['Cantón'].isin(top)]
        ct = pd.crosstab(df_sub['Cantón'], df_sub['Rural o urbano'])
        sns.heatmap(ct, annot=True, fmt="d", cmap="Reds")
        plt.title('Top 20 Cantones vs Zona')
        plt.show()

    def comparar_accidente_clima(self):
        plt.figure(figsize=(14, 7))
        ct = pd.crosstab(self.df['Tipo de accidente'], self.df['Estado del tiempo'], normalize='index') * 100
        ct.plot(kind='bar', stacked=True, colormap='viridis')
        plt.title('Tipo de Accidente vs Estado del Tiempo')
        plt.ylabel('Porcentaje (%)')
        plt.xlabel('Tipo de Accidente')
        plt.legend(title='Clima', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()