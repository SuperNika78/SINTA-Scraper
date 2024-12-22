 # 1. Journal distribution by affiliation
        plt.figure(figsize=(12, 6))
        affiliation_counts = df['affiliation'].value_counts().head(10)
        sns.barplot(x=affiliation_counts.values, y=affiliation_counts.index)
        plt.title('Top 10 Affiliations by Number of Journals')
        plt.xlabel('Number of Journals')
        plt.tight_layout()
        plt.savefig(os.path.join(self.viz_dir, 'affiliation_distribution.png'))
        plt.close()
        
        # 2. Accreditation distribution
        plt.figure(figsize=(8, 8))
        df['accreditation'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Distribution of Journal Accreditations')
        plt.axis('equal')
        plt.savefig(os.path.join(self.viz_dir, 'accreditation_distribution.png'))
        plt.close()