from rest_framework import serializers
from .models import User, Expense, ExpenseParticipant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone_number']

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    
    class Meta:
        model = ExpenseParticipant
        fields = ['user_email', 'amount']
        extra_kwargs = {
            'amount': {'required': False}
        }

class ExpenseSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(source='created_by.email')
    participants = ExpenseParticipantSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'created_by_email', 'total_amount', 'split_type', 'participants', 'date_created']

    def validate(self, data):
        if data['split_type'] == 'exact':
            for participant in data['participants']:
                if 'amount' not in participant:
                    raise serializers.ValidationError("Amount is required for each participant when split type is exact.")
        elif data['split_type'] == 'percentage':
            total_percentage = sum(participant['amount'] for participant in data['participants'])
            if total_percentage != 100:
                raise serializers.ValidationError("Total percentage must equal 100.")
        return data

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        created_by_email = validated_data.pop('created_by')['email']
        created_by = User.objects.get(email=created_by_email)
        split_type = validated_data.pop('split_type')
        expense = Expense.objects.create(created_by=created_by, split_type=split_type, **validated_data)
        
        if split_type == 'equal':
            split_amount = validated_data['total_amount'] / len(participants_data)
            for participant_data in participants_data:
                user_email = participant_data['user']['email']
                user, _ = User.objects.get_or_create(email=user_email)
                ExpenseParticipant.objects.create(expense=expense, user=user, amount=split_amount)
        
        elif split_type == 'exact':
            for participant_data in participants_data:
                user_email = participant_data['user']['email']
                amount = participant_data['amount']
                user, _ = User.objects.get_or_create(email=user_email)
                ExpenseParticipant.objects.create(expense=expense, user=user, amount=amount)

        elif split_type == 'percentage':
            for participant_data in participants_data:
                user_email = participant_data['user']['email']
                percentage = participant_data['amount'] / 100  # Assuming `amount` here represents percentage
                amount = validated_data['total_amount'] * percentage
                user, _ = User.objects.get_or_create(email=user_email)
                ExpenseParticipant.objects.create(expense=expense, user=user, amount=amount)
        
        return expense
